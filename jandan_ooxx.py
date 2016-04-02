#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''爬煎蛋妹子图原图'''
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import os
global cnt
def url_open(url):
	req = Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0')
	response = urlopen(req)
	return response.read()
def get_pic(url):
	global cnt
	bs = BeautifulSoup(urlopen(url).read(), 'lxml')
	nameList = bs.findAll('a', {'class':'view_img_link'})
	for name in nameList:
		pic_url = name['href']
		with open(str(cnt)+'.jpg', 'wb') as fout:
			fout.write(url_open(pic_url))
		cnt = cnt+1
url = r'http://jandan.net/ooxx'
html = urlopen(url)
bs = BeautifulSoup(html.read(), 'lxml')
page = int(bs.find('span', {'class':'current-comment-page'}).get_text()[1:-1])
cnt = 1
try:
	os.mkdir('python_girl')
except:
	pass
os.chdir('python_girl')
for i in range(int(input('How many pages do you want?\n'))):
	target = url+r'/page-'+str(page)+'#comments'
	print(target)
	get_pic(target)
	page -= 1