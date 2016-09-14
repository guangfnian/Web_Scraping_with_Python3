import os
import shutil
import requests
from lxml import etree

def down_load(url, cnt):
    print('Getting No.%s  %s...' % (cnt, url))
    res = requests.get(url, stream = True)
    with open(cnt + '.jpg', 'wb') as fout:
        shutil.copyfileobj(res.raw, fout)

if __name__ == '__main__':
    url = input('Please Input the URL...\n')
    page = requests.get(url)
    html = etree.HTML(page.text)
    dir = os.path.join(os.getcwd(), 'dgtle', html.xpath('/html/head/title')[0].text)
    if not os.path.exists(dir):
        os.makedirs(dir)
    os.chdir(dir)
    pic_lists = html.xpath(r'//*[@id]/@zoomfile')
    cnt = 1
    for pic in pic_lists:
        down_load(pic, str(cnt))
        cnt += 1
