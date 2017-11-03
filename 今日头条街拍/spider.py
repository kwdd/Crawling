#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#抓取今日头条 街拍美图，抓取网站https://www.toutiao.com
#抓取ajax请求所获取的图片,运行结果存在img里
#执行前需要创建“toutiao数据库”和“toutiao1表”
#运行时只需更改get_page_index的两个参数即可

#引入Requests库 
import requests
#引入json库
import json
#引入正则表达式库
import re
#引入mysql库
import pymysql
#引入os库，用于获取当前路径
import os, sys
#引入md5库，防止图片重复下载
from hashlib import md5
#引入urllib库，用于将字典形式的数据变成url参数
from urllib.parse import urlencode
#引入异常处理
from requests.exceptions import RequestException
#页面解析库，将html格式化显示
from lxml import etree
#引入自定义的数据库配置
from config import *
#引入进程池，开启多线程
from multiprocessing import Pool

#请求函数，传入参数[页数offset，要查的关键字keyword]
def get_page_index(offset, keyword):
	data = {
		'offset': offset,
		'format': 'json',
		'keyword': keyword,
		'autoload': 'true',
		'count': '20',
		'cur_tab': 1
	}
	url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
	try:
		res = requests.get(url)
		res.encoding = res.apparent_encoding #用requests库的apparent_encoding方法，自动获取页面的字符集编码
		if res.status_code == 200:
			return res.text
		return None
	except RequestException:
		print('请求索引页出错')
		return None
#获取详情页信息
def get_page_detail(url):
	try:
		res = requests.get(url)
		res.encoding = res.apparent_encoding #用requests库的apparent_encoding方法，自动获取页面的字符集编码
		if res.status_code == 200:
			return res.text
		return None
	except RequestException:
		print('请求详情页出错')
		return None
#解析详情页的方法
def parse_page_detail(html, url):
	images_pattern = re.compile('title: .*?,', re.S)
	result = re.search(images_pattern, html)
	title=''
	if result:
		title = result.group(0)[result.group(0).find('\'') + 1:-2]
	images_pattern = re.compile('content: .*?,', re.S)
	result = re.search(images_pattern, html)
	contents = {}
	if result:
		images_pattern = re.compile('img src=&quot;.*?&quot;', re.S)
		contents = re.findall(images_pattern, result.group(0))
		for i in range(0, len(contents)):
			contents[i] = 'https:' + contents[i][14:-6]
	for image in contents: download_image(image)
	return {
		'title': title,
		'url': url,
		'images': contents
	}
#html返回数据解析函数
def parse_page_index(html):
	data = json.loads(html) #json.loads，将json字符串转化为对象
	if data and 'data' in data.keys(): #是否含有data,data.keys()返回键名
		for item in data.get('data'):
			yield item.get('article_url')
#存储到数据库
def save_to_mongo(result):
	try:
		conn =  pymysql.connect(**config)
		with conn.cursor() as cur:
			sql = 'insert into toutiao1 values("%s","%s","%s")' % (result['title'],result['url'],result['images'])
			cur.execute(sql)
			conn.commit()
			print (result['title'], '存储到数据库成功')
	except  Exception as err:
		print("查询失败", err)
#访问图片网站
def download_image(url):
	try:
		res = requests.get(url)
		res.encoding = res.apparent_encoding #用requests库的apparent_encoding方法，自动获取页面的字符集编码
		if res.status_code == 200:
			save_image(res.content)
		return None
	except RequestException:
		print('请求图片出错')
		return None
#保存图片到文件img里
def save_image(content):
	file_path = '{0}/img/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
	if not os.path.exists(file_path):
		with open(file_path, 'wb') as f:
			f.write(content)
			f.close()
			print(file_path,'图片存储成功')
#主函数
def main(offset):
	html = get_page_index(offset, KEYWORD)
	for url in parse_page_index(html):
		html = get_page_detail(url)
		if html:
			result = parse_page_detail(html, url)
			save_to_mongo(result)
#执行函数
if __name__ == '__main__':
	# main()
	groups = [x * 20 for x in range(GROUP_START, GROUP_END + 1)]
	pool = Pool()
	pool.map(main, groups)