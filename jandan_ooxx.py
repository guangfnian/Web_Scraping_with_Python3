'''爬煎蛋妹子图原图'''
import os
import shutil
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.91 Safari/537.36',
}

def download_pic(url, name):
    print('getting No.%s %s' % (name, url))
    res = requests.get(url, stream = True)
    with open(name + '.jpg', 'wb') as fout:
        shutil.copyfileobj(res.raw, fout)


def prase_page(url):
    page = requests.get(url, headers = headers)
    html = etree.HTML(page.text)
    pic_lists = html.xpath('//*[@id]/div[1]/div/div[2]/p/a/@href')
    cnt = 1
    for pic_url in pic_lists:
        download_pic(pic_url, str(cnt))
        cnt += 1

if __name__ == '__main__':
    url = r'http://jandan.net/ooxx'
    page = requests.get(url, headers = headers)
    html = etree.HTML(page.text)
    number = int(html.xpath('//*[@id="comments"]/div[2]/div/span')[0].text[1:-1])
    main_dir = os.path.join(os.getcwd(), 'jandan_ooxx')
    for i in range(int(input('How many pages do you want to get?\n'))):
        current_dir = os.path.join(main_dir, str(number))
        if not os.path.exists(current_dir):
            os.makedirs(current_dir)
        os.chdir(current_dir)
        target_url = url+r'/page-'+str(number)+'#comments'
        print('Now getting page %s...' % target_url)
        prase_page(target_url)
        number -= 1