import os
import shutil
import requests
from lxml import etree

def parse_name(name): # 处理windows系统下非法的目录字符
    black_list = ('\\', '/', ':', '*', '?', '"', '<', '>', '|') # 非法字符集
    name = ' '.join(name.split())
    name = ''.join(list(map(lambda x: '_' if x in black_list else x, name)))
    return name

def down_load(url, cnt): # download the target picture
    print('Getting No.%s  %s...' % (cnt, url))
    if os.path.exists(cnt + '.jpg'): # if exists, do nothing
        return
    res = requests.get(url, stream = True)
    with open(cnt + '.jpg', 'wb') as fout:
        shutil.copyfileobj(res.raw, fout)

if __name__ == '__main__':
    # example: http://www.dgtle.com/article-15808-1.html
    url = input('Please Input the URL...\n')
    page = requests.get(url)
    html = etree.HTML(page.text)
    dir = os.path.join(os.getcwd(), 'dgtle', parse_name(html.xpath('/html/head/title')[0].text)) # get the page title
    if not os.path.exists(dir): # creat the directory
        os.makedirs(dir)
    os.chdir(dir)
    pic_lists = html.xpath(r'//*[@id]/@zoomfile') # find all the pictures
    cnt = 1
    for pic in pic_lists:
        down_load(pic, str(cnt))
        cnt += 1
