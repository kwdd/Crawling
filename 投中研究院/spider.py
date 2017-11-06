#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#抓取投中研究院报告，抓取网站https://www.chinaventure.com.cn/cmsmodel/report/list.shtml
#抓取访问页面,抓取其pdf文档，下载至downpdf/tzyjy
#运行时需更换访问报告的参数，参数从单个报告的url中获取
#更新时间2017-11-6

#引入Requests库 
import requests
#引入正则表达式库
import re
#引入os库，用于获取当前路径
import os
#引入异常处理
from requests.exceptions import RequestException
#引入进程池，开启多线程
from multiprocessing import Pool
from urllib.parse import urlencode

#访问投中单个报告页面
def get_index_page(url):
    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('error:请求报告页出错')
        return None
#利用这则获取“报告下载的url和报告名称”
def parser_sub_html(html):

    title = re.findall(re.compile(r'<h1 class="h1_01" title=".*?">(.*?)</h1>', re.S), html)
    if title:
        title = ''.join(title).replace('/', '')
    url = re.findall(re.compile(r'href="(https://pic.chinaventure.com.cn//cms/.*?.pdf)"', re.S), html)
    if url:
        return ''.join(url), title
    else:
        return 'n'
#判断单个报告是否存在，如果存在返回y
def jud_file(title):
    filename = '/Users/zhaozk/Desktop/python/downpdf/tzyjy/%s.pdf' % title
    if os.path.exists(filename):
        return 'y'
#传入报告的名称和url，进行下载
def save_pdf(url, title):
	try:
	    con = requests.get(url).content
	    path = '/Users/zhaozk/Desktop/python/downpdf/tzyjy'
	    if not os.path.exists(path):
	        os.mkdir(path)
	    file_name = '{0}/{1}.{2}'.format(path, title, 'pdf')
	    if not os.path.exists(file_name):
	        with open(file_name, 'wb') as f:
	            f.write(con)
	            print('保存成功', title)
	except Exception as e:
		print('error:保存报告发生异常', e)
#主函数
def main(page):
	try:
		html = get_index_page(url='https://www.chinaventure.com.cn/cmsmodel/report/detail/%s.shtml' % page)
		if parser_sub_html(html) is not 'n':
			url, title = parser_sub_html(html)
			if jud_file(title) is not 'y':
				save_pdf(url, title)
			else:
				print(title, '文件已存在')
		else:
			print('没有下载url,图文结合的形式，https://www.chinaventure.com.cn/cmsmodel/report/detail/%s.shtml' % page)
	except Exception as e:
		print('error:主函数异常', e)
#执行函数
if __name__ == '__main__':
	groups = range(1321,1348)
	pool = Pool()
	pool.map(main, groups)
    # main(1321)