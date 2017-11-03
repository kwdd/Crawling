#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#抓取猫眼电影 榜单 top100，抓取网站http://maoyan.com/
#通过正则表达式来获取页面信息,运行结果存在result.txt内

#引入Requests库 
import requests
#引入正则表达式库
import re
#引入json库
import json
#引入异常处理
from requests.exceptions import RequestException
#引入多线程
from multiprocessing import Pool

#请求函数
def get_one_page(url):
	header = {
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
	}
	try:
		res = requests.get(url, headers=header)
		res.encoding = res.apparent_encoding #用requests库的apparent_encoding方法，自动获取页面的字符集编码
		if res.status_code == 200:
			return res.text
		return None
	except RequestException:
		return None
#正则匹配函数
def parse_one_page(html):
	pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
						+'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
						+'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
	items = re.findall(pattern, html)
	#格式化数据
	for item in items:
		yield{
			'index': item[0],
			'image': item[1],
			'title': item[2],
			'actor': item[3].strip()[3:], #strip()去掉换行符
			'time': item[4].strip()[5:],
			'score': item[5]+item[6]
		}
#将数据存储至文件
def write_to_file(content):
	with open('result.txt', 'a', encoding='utf-8') as f:
		f.write(json.dumps(content, ensure_ascii=False) + '\n')
		f.close()
#主函数
def main(offset):
	url = 'http://maoyan.com/board/4?offset=' + str(offset)
	html = get_one_page(url)
	for item in parse_one_page(html):
		print(item)
		write_to_file(item)
#执行函数
if __name__ == '__main__':
	pool = Pool()
	pool.map(main, [i*10 for i in range(10)])