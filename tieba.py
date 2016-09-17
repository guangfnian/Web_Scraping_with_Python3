import os
import shutil
import requests
from lxml import etree

def parse_name(name): # 处理windows系统下非法的目录字符
    black_list = ('\\', '/', ':', '*', '?', '"', '<', '>', '|') # 非法字符集
    name = ' '.join(name.split())
    name = ''.join(list(map(lambda x: '_' if x in black_list else x, name)))
    return name

def down_load(url, cnt):
    header = r'http://imgsrc.baidu.com/forum/pic/item/' # original source url header
    url = header + url.split(r'/')[-1]
    print('Getting No.%s  %s...' % (cnt, url))
    if os.path.exists(cnt + '.jpg'): # if exists, do nothing
        return
    res = requests.get(url, stream = True)
    with open(cnt + '.jpg', 'wb') as fout:
        shutil.copyfileobj(res.raw, fout)

if __name__ == '__main__':
    url = input('Please Input the URL...\n')
    page = requests.get(url)
    html = etree.HTML(page.text)
    dir = os.path.join(os.getcwd(), 'tieba', parse_name(html.xpath('/html/head/title')[0].text))
    if not os.path.exists(dir):
        os.makedirs(dir)
    os.chdir(dir)
    results = html.xpath('//*[@id]/img[@class="BDE_Image"]/@src') # find all pictures
    cnt = 1
    for pic_url in results:
        down_load(pic_url, str(cnt))
        cnt += 1
