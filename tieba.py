import os
import shutil
import requests
from lxml import etree

def down_load(url, cnt):
    header = r'http://imgsrc.baidu.com/forum/pic/item/'
    url = header + url.split(r'/')[-1]
    print('Getting No.%s  %s...' % (cnt, url))
    res = requests.get(url, stream = True)
    with open(cnt + '.jpg', 'wb') as fout:
        shutil.copyfileobj(res.raw, fout)

if __name__ == '__main__':
    url = input('Please Input the URL...\n')
    page = requests.get(url)
    html = etree.HTML(page.text)
    dir = os.path.join(os.getcwd(), 'tieba', html.xpath('/html/head/title')[0].text)
    if not os.path.exists(dir):
        os.makedirs(dir)
    os.chdir(dir)
    results = html.xpath('//*[@id]/img[@class="BDE_Image"]/@src')
    cnt = 1
    for pic_url in results:
        down_load(pic_url, str(cnt))
        cnt += 1
