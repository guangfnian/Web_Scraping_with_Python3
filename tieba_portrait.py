'''
百度贴吧用户头像原图爬虫（以该吧经验值从高到低开始爬）
'''
import os
import shutil
import requests
from lxml import etree

def download_usr_pic(url, name): # 获取并下载用户头像
    print('Getting %s...' % name)
    page = requests.get(url)
    html = etree.HTML(page.text)
    try:
        pic_url = html.xpath('//*[@id="j_userhead"]/a/img/@src')[0]
    except: # 部分用户主页无法访问，提示页面不存在
        print('404 Error!')
        return
    pic_url = r'http://himg.baidu.com/sys/portraitl/item/' + pic_url.split('/')[-1]
    res = requests.get(pic_url, stream = True)
    with open(name + '.jpg', 'wb') as fout:
        shutil.copyfileobj(res.raw, fout)

def get_usr_url(url): # 获取url页面上所有用户的个人主页地址
    page = requests.get(url)
    html = etree.HTML(page.text)
    usr_lists = html.xpath('//a[@class="drl_item_name_top"] | //a[@class="drl_item_name_nor"]')
    for usr in usr_lists:
        download_usr_pic(r'http://tieba.baidu.com'+usr.get('href'), usr.text)

if __name__ == '__main__':
    tieba_name = input('Please input the name of tieba...\n')
    dir = os.path.join(os.getcwd(), 'tieba_portrait', tieba_name)
    if not os.path.exists(dir):
        os.makedirs(dir)
    os.chdir(dir)
    tieba_name = str(tieba_name.encode('GB2312')).replace(r'\x','%').split("'")[1]#进行网址的GB2312编码
    pages = int(input('How many pages ?\n'))
    url = r'http://tieba.baidu.com/f/like/furank?kw=' + tieba_name + '&pn=';
    for i in range(1, pages+1):
        get_usr_url(url+str(i))