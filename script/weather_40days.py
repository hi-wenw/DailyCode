# -*- coding: utf-8 -*-
import pandas as pd
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # 读取城市编码文档
    df = pd.read_csv('cityCode.csv')
    # 读取广东地区城市编码
    gd_df = df[(df['city_code'] > 101280000) & (df['city_code'] < 101290000)]

    # for i in gd_df.values.tolist():
    #     url = f'http://www.weather.com.cn/weather40dn/{i[1]}.shtml'
    #     response = requests.get(url)
    #     response.encoding = 'utf8'
    #     print(response.text.encode('utf-8').decode('utf-8').encode('gbk', 'ignore').decode('gbk'))

    url = f'http://www.weather.com.cn/weather40d/{gd_df.values.tolist()[0][1]}.shtml'
    response = requests.get(url)
    response.encoding = 'utf8'
    requests_text = response.text.encode('utf-8').decode('utf-8').encode('gbk', 'ignore').decode('gbk')
    soup = BeautifulSoup(requests_text, 'lxml')
    table = soup.find_all('div', class_='W_left')[1]

    field = table.find_all('tr')[1:]
    for i in field:
        td_tags = i.find_all('td')
        for td_tag in td_tags:
            h2_tag = td_tag.find('h2')
            if h2_tag:
                date = h2_tag.find('span', class_='nowday orange').text.strip()
                print('日期：{}'.format(date))

                max_temp = td_tag.find('span', class_='max').text.strip()
                min_temp = td_tag.find('span', class_='min').text.strip()
                print('最高温度：{}，最低温度：{}'.format(max_temp, min_temp))

                other_info = td_tag.find('div', class_='w_xian').find_all('span', class_=None)
                precipitation_probability = other_info[0].text.strip()
                text = other_info[1].text.strip()
                print('降水概率：{}，天气情况：{}'.format(precipitation_probability, text))
