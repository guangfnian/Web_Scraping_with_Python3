#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
百度贴吧用户头像原图爬虫（以该吧经验值从高到低开始爬）
'''
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import os
def download_usr_pic(url, name):#获取并下载用户头像
	html = urlopen(url)
	bs = BeautifulSoup(html.read(), 'lxml')
	pics = bs.findAll('a', {'class':'userinfo_head'})[0]
	for pic in pics:
		pic_url = r'http://himg.baidu.com/sys/portraitl/item/'+pic['src'].split('/')[-1].split('?')[0]#头像原图地址
		with open(name+'.jpg', 'wb') as fout:
			fout.write(urlopen(pic_url).read())
			print(name, '....ok')

def get_usr_url(url):#获取url页面上所有用户的个人主页地址
	html = urlopen(url)
	bs = BeautifulSoup(html.read(), 'lxml')
	usrs = bs.findAll('a', {'class':'drl_item_name_top'}) + bs.findAll('a', {'class':'drl_item_name_nor'})
	for usr in usrs:
		download_usr_pic(r'http://tieba.baidu.com'+usr['href'], usr.get_text())

dir = 'tieba_portrait'
try:
	os.mkdir(dir)
except:
	pass
os.chdir(dir)
tieba_name = input('Please input the name of tieba...\n')
tieba_name = str(tieba_name.encode('GB2312')).replace(r'\x','%').split("'")[1]#进行网址的GB2312编码
pages = int(input('How many pages do you want?\n'))
url = r'http://tieba.baidu.com/f/like/furank?kw=' + tieba_name + '&pn=';
for i in range(1, pages+1):
	get_usr_url(url+str(i))