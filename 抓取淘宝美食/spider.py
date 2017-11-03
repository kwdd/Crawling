#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#抓取淘宝美食图片，抓取网站https://www.taobao.com
#使用Selenium+Chrome/PhantomJS抓取
#此脚本爬取淘宝的美食商品信息，如若改变爬取内容，请到config内改变
#引入正则表达式库
import re
#引入pyquery库，解析源代码
from pyquery import PyQuery as pq
#引入selenium插件，实现模拟鼠标操作网页
from selenium import webdriver
#引入等待响应
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#引入异常处理
from requests.exceptions import RequestException
#引入自定义的数据库配置
from config import *

#初始化网页
# broweser = webdriver.Chrome()
# 使用PhantomJS
broweser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
#设置PhantomJS窗口的大小
broweser.set_window_size(1400, 900)
#设定全局变量，方便使用
wait = WebDriverWait(broweser, 10)
#创建搜索方法，实现模拟打开淘宝页面，并搜索美食
def search():
	print('正在搜索')
	try:
		broweser.get('https://www.taobao.com')
		input = wait.until(
			EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
		)
		submit = wait.until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
		) 
		input.send_keys(KEYWORD)
		submit.click()
		total = wait.until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total'))
		)
		get_projects()
		return total.text
	except TimeoutException:
		return search()
#实现翻页操作，传入参数为要翻的页码
def next_page(page_number):
	print('正在翻页', page_number)
	try:
		input = wait.until(
			EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
		)
		submit = wait.until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
		)
		input.clear()
		input.send_keys(page_number)
		submit.click()
		#该元素中有这样的文字
		wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
		get_projects()
	except TimeoutException:
		return next_page(page_number)
#抓取页面图片信息
def get_projects():
	#判断宝贝信息是否加载成功
	wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
	#获取页面源代码
	html = broweser.page_source
	#解析下页面源代码
	doc = pq(html)
	#选出所有的item
	items = doc('#mainsrp-itemlist .items .item').items()
	for item in items:
		product = {
			'image': item.find('.pic .img').attr('src'),
			'price': item.find('.price').text(),
			'deal': item.find('.deal-cnt').text()[:-3],
			'title': item.find('.title').text(),
			'shop': item.find('.shop').text(),
			'location': item.find('.location').text()
		}
		save_to_mongo(product)
#存储到数据库
def save_to_mongo(result):
	try:
		conn =  pymysql.connect(**config)
		with conn.cursor() as cur:
			sql = 'insert into taobao values("%s","%s","%s","%s","%s","%s")' % (result['image'],result['price'],result['deal'],result['title'],result['shop'],result['location'])
			cur.execute(sql)
			conn.commit()
			print ('插入成功', result['title'])
	except  Exception as err:
		print("查询失败", err)
#主函数
def main():
	try:
		total = search()
		total = int(re.compile('(\d+)').search(total).group(1))
		for i in range(2, total + 1):
			next_page(i)
	#无论出不出现异常都将执行finally
	except  Exception as err:
		print("出错了", err)
	finally:
		broweser.close()
#执行函数
if __name__ == '__main__':
	main()