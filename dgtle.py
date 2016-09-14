import os
import shutil
import requests
from lxml import etree

def down_load(url, cnt): # download the target picture
    print('Getting No.%s  %s...' % (cnt, url))
    res = requests.get(url, stream = True)
    with open(cnt + '.jpg', 'wb') as fout:
        shutil.copyfileobj(res.raw, fout)

if __name__ == '__main__':
    # example: http://www.dgtle.com/article-15808-1.html
    url = input('Please Input the URL...\n')
    page = requests.get(url)
    html = etree.HTML(page.text)
    dir = os.path.join(os.getcwd(), 'dgtle', html.xpath('/html/head/title')[0].text) # get the page title
    if not os.path.exists(dir): # creat the directory
        os.makedirs(dir)
    os.chdir(dir)
    pic_lists = html.xpath(r'//*[@id]/@zoomfile') # find all the pictures
    cnt = 1
    for pic in pic_lists:
        down_load(pic, str(cnt))
        cnt += 1
