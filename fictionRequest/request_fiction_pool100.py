# -*- coding: utf-8 -*-
import datetime
import threading
import requests
from bs4 import BeautifulSoup
import os
import queue
from concurrent.futures import ThreadPoolExecutor


def get_chapter_data(chapter_list):
    global num
    with lock:
        current_num = num
        num += 1

    response2 = requests.get(chapter_list[1], headers=headers)
    response2.encoding = 'utf8'
    soup2 = BeautifulSoup(response2.text, 'lxml')
    try:
        with open(f'{dt}/{current_num}_{chapter_list[0]}.txt', 'w', encoding='utf8') as f:
            f.write(soup2.find('div', {'id': 'content'}).text.strip().replace(" ", "").replace("\n", ""))
        print(f'爬取 {chapter_list[0]} 成功,{datetime.datetime.now()},{threading.currentThread().name}')
    except OSError:
        with open(f'{dt}/{current_num}_.txt', 'w', encoding='utf8') as f:
            f.write(soup2.find('div', {'id': 'content'}).text.strip().replace(" ", "").replace("\n", ""))
        print('跳过')


if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=100)
    queue_list = queue.Queue()
    lock = threading.Lock()

    url = 'https://www.biquger.cc/book/1234/'
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

    # 标题 检查是否存在目录 不存在则创建
    dt = str(soup.find_all('div', {'id': 'list'})[1].find('dt').text)
    try:
        os.mkdir(dt)
    except FileExistsError:
        print('目录已存在')

    chapter = soup.find_all('div', {'id': 'list'})[1].find_all('a')

    num = 1

    for i in chapter:
        url = f"https://www.biquger.cc/book/1234/{i['href'].split('/')[-1]}"
        queue_list.put([i.text.strip(), url])

    for i in range(queue_list.qsize()):
        pool.submit(get_chapter_data, queue_list.get())
