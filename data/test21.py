# -*- coding: gbk -*-
import logging

import requests
import pandas as pd


def weather_request(areacode):
    url = "https://eolink.o.apispace.com/456456/weather/v001/day"
    payload = {"days": "15", "areacode": areacode}
    headers = {
        "X-APISpace-Token": "qgx41bu8a8kvrjov8tb5wb09r6x000it",
        "Authorization-Type": "apikey"
    }

    response = requests.request("GET", url, params=payload, headers=headers)

    logging.info('未来15天天气' + response.text)


# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO,                 # 创建日志对象
#                         format='%(asctime)s - %(levelname)s - %(message)s',
#                         filename='weather.txt',
#                         filemode='w')
#     df = pd.read_csv(r'C:\Users\Administrator\PycharmProjects\pythonProject\weather\areaCode.csv',encoding='gbk')
#     province_df = df.query('exclude > 0').query('areacode < 101080902')
#
#     for i in province_df['areacode']:
#         logging.info('城市编码:'+str(i))
#         weather_request(i)
import pandas as pd

# 创建示例DataFrame
data = {'A': [1, 2, 3],
        'B': [4, 5, 6],
        'C': [7, 8, 9]}
df = pd.DataFrame(data)

# 指定新的列顺序
new_order = ['B', 'A', 'C']

# 使用reindex()方法重新排列列
df = df.reindex(columns=new_order)

# 打印修改后的DataFrame
print(df)
