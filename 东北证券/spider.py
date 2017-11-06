#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#抓取东北证券，抓取网站http://www.nesc.cn/classHTML/0001000100020002000600070004.html
#抓取ajax请求所获取的页面,抓取其pdf文档，下载至
#运行时只需更改get_page_index的[页面page]参数即可
#更新时间2017-11-2

#引入Requests库，用于格式化html代码
import requests
#引入os库，用于获取当前路径
import os
#引入json库
import json
#引入正则表达式库
import re
#引入进程池，开启多线程
from multiprocessing import Pool
#引入异常处理
from requests.exceptions import RequestException

#访问东北证券的行业研究页面，post请求函数，传入参数[页数page]
def post_index_page(page):
    url = 'http://www.nesc.cn/classHTML/0001000100020002000600070004.html'
    data = {
        'classid': '0001000100020002000600070004',
        'pageSize': '12',
        'pageIndex': page,
        'totalCounts': '0',
        'flag': '1',
        'childclassid': '',
        'static': 'false'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Referer': 'http://www.nesc.cn/dbzq/public/list.jsp?classid=0001000100020002000600070004'
    }
    try:
        res = requests.post(url, data=data, headers=headers)
        res.encoding = res.apparent_encoding
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None
#传入post_index_page返回的结果，对结果做简单处理，取出每篇报告的'题目'和'对应的id'
def parser_index_html(html):
    data = json.loads(html)
    for item in data['result']:
        yield{
            'id': item['infoId'],
            'title': item['title']
        }
#传入每篇报告的'题目'和'对应的id'，访问单个报告页面，返回json串
def post_sub_html(item):
    data = {
        'action': 'getInfoDetail',
        'infoid': item['id']
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        response = requests.post(url='http://www.nesc.cn/JSONService/webService/infoService.jsp', data=data, headers=headers)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求',item['title'],'报告页面出错')
        return None
#传入post_sub_html返回的结果、题头，对json串进行处理，获取并请求pdf报告网页版，返回2进制串
def parser_sub_html(html,item):
    try:
        pattern = re.compile('filepath.*?,', re.S)
        items = re.search(pattern, html)
        if items:
            return requests.get('http://www.nesc.cn/' + items.group(0)[11:-2]).content
        else:
            return None
    except RequestException:
        print('获取',item['title'],'报告内容出错')
        return None
#判断单个报告是否存在，如果存在返回y
def jud_file(con):
    filename = '/Users/zhaozk/Desktop/python/downpdf/dbzq/%s.pdf' % con['title']
    if os.path.exists(filename):
        return 'y'
#将二进制内容，存储到'题目.pdf'文件里
def down_file(contents, title):
    try:
        file_path = '/Users/zhaozk/Desktop/python/downpdf/dbzq'
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        file_name = '{0}/{1}.{2}'.format(file_path, title, 'pdf')
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
        html = post_index_page(page)
        for item in parser_index_html(html):
            if jud_file(item) is not 'y':
                sub_html = post_sub_html(item)
                contents = parser_sub_html(sub_html,item)
                if contents:
                    down_file(contents, item['title'])
                else:
                    print(item['title'],' 没有内容')
            else:
                print(item['title'],'文件已存在')
    except Exception as e:
        print('主函数异常', e)
#执行函数
if __name__ == '__main__':
    main(1)
