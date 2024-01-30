# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = 'http://www.weather.com.cn/textFC/hn.shtml'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
    response = requests.get(url, headers=headers)

    response.encoding = 'utf8'

    soup = BeautifulSoup(response.text, 'lxml')

    # agg_Data = soup.find_all('div', class_='conMidtab2')  # 华南地区全省天气

    # for result in agg_Data:
    #     result = result.find('table').find_all('tr')[2:]
    #
    #     for i in result:
    #         result2 = i.find_all('td')[:-1]
    #         ls = []
    #         for j in result2:
    #             ls.append(j.text.strip().replace('\n', ' '))
    #         print(ls)

    result = soup.find_all('div', class_='conMidtab2')[1]

    # result = result.find_all('td', class_='rowsPan')
    result = result.find('table').find_all('tr')[2:]

    for i in result:
        result2 = i.find_all('td')[:-1]
        ls = []
        for j in result2:
            ls.append(j.text.strip().replace('\n', ' '))
        print(ls)
