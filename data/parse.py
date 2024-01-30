#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/10/20 21:05
# @Author  : 甚平
# -*- coding: gbk -*-
import datetime
import json
import logging
import pandas as pd
import requests


# 爬取对应城市15天天气数据
def weather_request(areacode):
    url = "https://eolink.o.apispace.com/456456/weather/v001/day"
    payload = {"days": "15", "areacode": areacode}
    headers = {
        "X-APISpace-Token": "lp8d8zt893qzk0gjzb5ca3u1gnj9symh",
        "Authorization-Type": "apikey"
    }

    cnt = 1
    while cnt < 4:
        try:
            response = requests.request("GET", url, params=payload, headers=headers, timeout=30)
            logging.info(f'>>>>> 爬取成功')
            return response
        except requests.Timeout:
            logging.warning(f'***** 爬取失败,开始第{cnt}次重试')
            cnt += 1
            if cnt == 4:
                logging.error(f'@@@@@ 多次爬取失败,告警!')


# 读取维度文件获取城市数据
def get_city_data():
    logging.info('>>>>> 程序开始执行,开始读取数据源')
    # 读取数据源,获取 城市编码,省份所属大区,省份,城市
    f = open('/data/project/fmdws/dim_area.csv', 'r', encoding='gbk')
    area_csv = f.read().strip().split('\n')
    f.close()
    logging.info('>>>>> 读取成功,获取市级粒度相关数据')
    city_list = []
    for i in area_csv:
        # 判断是否为市级地区
        if i.split(",")[12] == str(1):
            city_list.append([i.split(",")[0], i.split(",")[1], i.split(",")[3], i.split(",")[5]])
    logging.info('>>>>> 市级数据已获取,开始连接api爬取信息')
    return city_list


# 传入城市列表获取城市15天天气
def get_city_weather_data(city_list):
    weather_data = []  # 各地市天气数据存放位置
    for i in range(len(city_list)):  # 遍历市级数据列表,爬取天气数据
        city_code = int(city_list[i][0])
        logging.info(f'开始爬取<{city_list[i][1]}> <{city_list[i][2]}> <{city_list[i][3]}>')
        try:
            request_data = json.loads(weather_request(city_code).text)
            wea_ls = [city_list[i][1], city_list[i][2], city_list[i][3]]  # 用于存放本次遍历的地市级信息
            for result in request_data['result']['daily_fcsts']:  # 遍历获取天气信息加入wea_ls
                wea_ls.append(result['high'])
                wea_ls.append(result['low'])
                wea_ls.append(result['text_day'])
            weather_data.append(wea_ls)  # 添加本条地市天气信息至总数据列表

        except AttributeError:
            pass
    return weather_data


# 存入至csv文件
def save_to_csv(weather_data):
    # 转为DataFrame并更换列顺序
    df = pd.DataFrame(data=weather_data,
                      columns=['area', 'province', 'city',
                               'd_high_1', 'd_low_1', 'd_wea_1',
                               'd_high_2', 'd_low_2', 'd_wea_2',
                               'd_high_3', 'd_low_3', 'd_wea_3',
                               'd_high_4', 'd_low_4', 'd_wea_4',
                               'd_high_5', 'd_low_5', 'd_wea_5',
                               'd_high_6', 'd_low_6', 'd_wea_6',
                               'd_high_7', 'd_low_7', 'd_wea_7',
                               'd_high_8', 'd_low_8', 'd_wea_8',
                               'd_high_9', 'd_low_9', 'd_wea_9',
                               'd_high_10', 'd_low_10', 'd_wea_10',
                               'd_high_11', 'd_low_11', 'd_wea_11',
                               'd_high_12', 'd_low_12', 'd_wea_12',
                               'd_high_13', 'd_low_13', 'd_wea_13',
                               'd_high_14', 'd_low_14', 'd_wea_14',
                               'd_high_15', 'd_low_15', 'd_wea_15',
                               ])

    # 重新排序列
    df = df.reindex(columns=['area', 'province', 'city',
                             'd_high_1', 'd_low_1', 'd_high_2',
                             'd_low_2', 'd_high_3', 'd_low_3',
                             'd_high_4', 'd_low_4', 'd_high_5',
                             'd_low_5', 'd_high_6', 'd_low_6',
                             'd_high_7', 'd_low_7', 'd_high_8',
                             'd_low_8', 'd_high_9', 'd_low_9',
                             'd_high_10', 'd_low_10', 'd_high_11',
                             'd_low_11', 'd_high_12', 'd_low_12',
                             'd_high_13', 'd_low_13', 'd_high_14',
                             'd_low_14', 'd_high_15', 'd_low_15',
                             'd_wea_1', 'd_wea_2', 'd_wea_3',
                             'd_wea_4', 'd_wea_5', 'd_wea_6',
                             'd_wea_7', 'd_wea_8', 'd_wea_9',
                             'd_wea_10', 'd_wea_11', 'd_wea_12',
                             'd_wea_13', 'd_wea_14', 'd_wea_15'])
    df = df.drop_duplicates(subset=['area', 'province', 'city'])  # 以地区省市去重
    logging.info(f'>>>>> 所有城市已爬取,本次爬取城市{df.shape[0]}个,开始写入数据')
    df.to_csv('/data/project/fmdws/file_for_obs/huawei_weather_records.csv', index=False, header=False)  # 写入CSV
    logging.info('>>>>> 写入完成,程序运行结束')


def main():
    city_list = get_city_data()  # 读取维度数据
    weather_data = get_city_weather_data(city_list)  # 爬取天气数据
    save_to_csv(weather_data)  # 存入至CSV文件


# 配置日志参数
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=f'/data/project/fmdws/log/{str(datetime.datetime.today())[:10]}_weather_log.txt',
                    filemode='w')

if __name__ == '__main__':
    main()
