import os
import requests
import binascii
from lxml import etree

photo_type = { # 图片格式
    '47494638': '.gif',
    'ffd8ffe0': '.jpg',
    'ffd8ffe1': '.jpg',
    'ffd8ffdb': '.jpg',
    '89504e47': '.png'
}

def down_load(url, cnt):
    header = r'http://imgsrc.baidu.com/forum/pic/item/'
    url = header + url.split(r'/')[-1]
    print('Getting No.%s  %s...' % (cnt, url))
    res = requests.get(url, stream = True).content
    fmt = binascii.b2a_hex(res[0:4])  # 读取前4字节转化为16进制字符串
    ext = photo_type.get(str(fmt, 'utf-8'), '.jpg') # 默认按jpg处理
    with open(cnt + ext, 'wb') as fout:
        fout.write(res)

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
