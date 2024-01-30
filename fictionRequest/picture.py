# -*- coding: utf-8 -*-

import os
import queue
import threading
from urllib.parse import quote, unquote
import pyautogui
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


def get_picture(data):
    # with lock:
    img_response = requests.get(data[0], headers=headers)
    with open(data[1], 'wb') as f:
        f.write(img_response.content)
        print(f'Saved image: {data[1]}')


# 需要查询的内容
text = pyautogui.prompt(text='输入需要爬取图片的标题', title='', default='').strip()
print(text)
text_quote = quote(text, safe='')
print(text_quote)
if __name__ == '__main__':
    queue_list = queue.Queue()
    pool = ThreadPoolExecutor(max_workers=10)
    lock = threading.Lock()
    url = f'https://image.baidu.com/search/index?tn=baiduimage&word=%E8%8B%B9%E6%9E%9C'
    dir_name = text

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Referer": "https://www.google.com/",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Content-Type": "application/x-www-form-urlencoded",
        # 添加更多头部信息...
    }
    response = requests.get(url, headers=headers)

    response.encoding = 'utf8'

    soup = BeautifulSoup(response.text, 'lxml')
    print(soup)
    all_images = soup.find_all('img')
    print(all_images)
    # if response.status_code == 200:
    #     if not os.path.exists(dir_name):
    #         os.makedirs(dir_name)
    #
    # for image in all_images:
    #     img_url = image.get('src')
    #     if img_url.startswith(('http://', 'https://', '//')):
    #         if img_url.startswith('//'):
    #             img_url = f'https:{img_url}'
    #         img_name = img_url.split('/')[-1]
    #         img_path = os.path.join(dir_name, img_name)
    #         if '.' not in img_path:
    #             img_path += '.jpg'
    #         queue_list.put([img_url, img_path])
    #
    #     else:
    #         print('Failed to retrieve the webpage.')
    #
    # for i in range(queue_list.qsize()):
    #     pool.submit(get_picture, queue_list.get())
