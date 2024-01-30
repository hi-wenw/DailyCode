# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os

if __name__ == '__main__':
    url = 'https://www.biquger.cc/book/99/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
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
        url = f"https://www.biquger.cc/book/99/{i['href'].split('/')[-1]}"
        response2 = requests.get(url, headers=headers)
        response2.encoding = 'utf8'
        soup2 = BeautifulSoup(response2.text, 'lxml')

        try:
            with open(f'{dt}/{num}_{i.text.strip()}.txt', 'w', encoding='utf8') as f:
                f.write(soup2.find('div', {'id': 'content'}).text.strip().replace(" ", "").replace("\n", ""))
            print(f'爬取 {i.text.strip()} 成功')
        except OSError:
            print('跳过')
        num += 1
