#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#抓取中国证监会，抓取网站http://www.csrc.gov.cn/pub/newsite/xxpl/yxpl/
#抓取ajax请求所获取的页面,抓取其pdf文档，下载至
#运行时只需更改get_page_index的[页面page]参数即可
#更新时间2017-11-2

#引入Requests库 
import requests
#引入正则表达式库
import re
#引入os库，用于获取当前路径
import os
#引入进程池，开启多线程
from multiprocessing import Pool
#引入lxml可以直接通过html页面获取url
from lxml import etree
#引入异常处理
from requests.exceptions import RequestException

#访问证券监督委员会的预先披露页面，传入参数[页数offset，要查的关键字keyword]
def get_index_page(url):
    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求页面发生异常')
        return None
#格式化html页面，将每个“招股说明书【报告的名字和url】”截取下来
def parser_index_html(html):
    html = etree.HTML(html)
    title = html.xpath('//ul[@id="myul"]/li/a/text()')
    url = html.xpath('//ul[@id="myul"]/li/a/@href')
    num = 0
    for i in title:
        urls = url[num]
        url_list = 'http://www.csrc.gov.cn/pub' + urls[8:]
        yield {
            'title': i,
            'url': url_list
        }
        num += 1
#格式化报告页面，获取pdf查看页面的url
def parser_sub_html(html):
    html = etree.HTML(html)
    contents = html.xpath('//div[@class="content"]/a/@href')
    for con in contents:
        urls = con.replace('./', '')
        yield {
            'url': urls
        }
#判断单个招股说明书是否存在，如果存在返回y
def jud_file(con):
    filename = '/Users/zhaozk/Desktop/python/downpdf/zgjzh/%s.pdf' % con['title']
    if os.path.exists(filename):
        return 'y'
#传入招股说明书的名称和url，进行下载
def save_pdf(con, contents):
    contents = requests.get(contents).content
    name = con['title']
    try:
        file_path = '/Users/zhaozk/Desktop/python/downpdf/zgjzh'
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        file_name = '{0}/{1}.{2}'.format(file_path, name, 'pdf')
        if not os.path.exists(file_name):
            with open(file_name, 'wb') as f:
                f.write(contents)
                f.close()
                print('保存成功', file_name)
    except Exception as e:
        print('保存报告发生异常', e)
#主函数
def main(page):
    try:
        url_in = 'http://www.csrc.gov.cn/pub/newsite/xxpl/yxpl/index_%s.html' % page
        if page is 0:
            url_in = 'http://www.csrc.gov.cn/pub/newsite/xxpl/yxpl/index.html'
        html = get_index_page(url=url_in)
        for con in parser_index_html(html):
            if jud_file(con) is not 'y':
                sub_html = get_index_page(con['url'])
                for cons in parser_sub_html(sub_html):
                    index_url = con['url']
                    url_q = '/'.join(index_url.replace('http://', '').split('/')[:-1])
                    url_cons = ('http://' + url_q + '/' + cons['url'])
                    save_pdf(con, url_cons)
            else:
                print(con['title'],'文件已存在')
    except Exception as e:
        print('主函数异常', e)
#执行函数
if __name__ == '__main__':
    main(0)

