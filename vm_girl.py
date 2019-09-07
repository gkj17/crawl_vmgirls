import requests
from bs4 import BeautifulSoup
import os
import time

index = 0


def get_html(url, code='utf-8'):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    r.encoding = code
    print('Success')
    return r.text


def classify(html):
    global index
    number = 0
    soup = BeautifulSoup(html, 'html.parser')
    sitemap = soup.find_all('div', id='content', limit=2)

    # 最新文章
    article = sitemap[0].find_all('li')
    for i in article[0:]:  # 从第几个开始，一共一千个左右
        index = 0
        href = i.find('a').get('href')
        title = i.find('a').get('title')
        create_dir(os.path.join('E:\PycharmProjects\scrapyproject\Vm_girls\latest_article\{}'.format(title)))
        print('No.{}'.format(number)+title)
        download_pic(href, title)
        number += 1

    number = 0
    # 分类目录
    menu = ['campus', 'fresh', 'pure', 'sweet', 'youth', 'photography']
    for type_ in menu:
        create_dir(os.path.join('E:\PycharmProjects\scrapyproject\Vm_girls\{}'.format(type_)))
        url = 'https://www.vmgirls.com/{}'.format(type_)
        soup_ = BeautifulSoup(get_html(url), 'html.parser')
        page = soup_.find_all('div', class_='list-body')

        for i in page:
            '''下载进入页面就有的几个相册'''
            href_ = i.find('a').get('href')
            title_ = i.get_text()
            print('{} No.{}'.format(type_, number) + title_)
            download_pic_(href_, title_, str(type_))
            number += 1

        # for i in range(2, 7):
        #     data = {
        #         'append': 'list - archive',
        #         'paged': '{}'.format(i),
        #         'action': 'ajax_load_posts',
        #         'query': '17',
        #         'page': 'cat'
        #     }
        #     header_ajax = {
        #         'authority': 'www.vmgirls.com',
        #         'method': 'POST',
        #         'path': '/wp-admin/admin-ajax.php',
        #         'scheme': 'https',
        #         'Accept': 'text/html, */*; q=0.01',
        #         'Accept-encoding': 'gzip, deflate, br',
        #         'Accept-language': 'zh-CN,zh;q=0.9',
        #         'Content-length': '68',
        #         'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #         'Cookie': 'Hm_lvt_a5eba7a40c339f057e1c5b5ac4ab4cc9=1567325369,1567826213,1567854872; PHPSESSID=8bu73jb7lrv22kucug5q2qvl6a; Hm_lpvt_a5eba7a40c339f057e1c5b5ac4ab4cc9=1567855774',
        #         'Origin': 'https://www.vmgirls.com',
        #         'Referer': 'https://www.vmgirls.com/photography',
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36 chrome-extension',
        #         'X-requested-with': 'XMLHttpRequest'
        #     }
        #     json = requests.post('https://www.vmgirls.com/wp-admin/admin-ajax.php', data, headers=header_ajax)
        #     print(json)


def download_pic(url, name):
    '''for latest articles'''
    global index
    soup = BeautifulSoup(get_html(url), 'html.parser')
    post = soup.find('div', class_='post-content').find('div', class_='nc-light-gallery').find('p')
    for i in post.find_all('a'):
        girls = i.find('img')
        girl = girls.get('data-src')
        with open('vm_girls/latest_article/{}/{}.{}'.format(name, index, girl[len(girl)-3:len(girl)]), 'wb') as f:
            f.write(requests.get(girl).content)
            time.sleep(0.3)
            print('{}'.format(index))
        index += 1


def download_pic_(url, name, type_):
    '''for category'''
    global index
    soup = BeautifulSoup(get_html(url), 'html.parser')
    post = soup.find('div', class_='post-content').find('div', class_='nc-light-gallery').find('p')
    if not post.find_all('a'):
        iter_ = soup.find('div', class_='post-content').find('div', class_='nc-light-gallery').find_all('p')[1:]
    else:
        iter_ = post.find_all('a')
    for i in iter_:
        girls = i.find('img')
        girl = girls.get('data-src')
        name = name.replace('\n', '')
        name = name.replace(' ', '')
        create_dir(os.path.join('E:\PycharmProjects\scrapyproject\Vm_girls\{}\{}'.format(type_, name)))
        with open('vm_girls/{}/{}/{}.{}'.format(type_, name, index, girl[len(girl)-3:len(girl)]), 'wb') as f:
            f.write(requests.get(girl).content)
            time.sleep(0.3)
            print('{}'.format(index))
        index += 1


def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)


if __name__ == '__main__':
    create_dir('Vm_girls')
    create_dir(os.path.join('E:\PycharmProjects\scrapyproject\Vm_girls\latest_article'))

    url = 'https://www.vmgirls.com/sitemap.shtml'
    html = get_html(url)
    classify(html)