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

    logging.info('δ��15������' + response.text)


# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO,                 # ������־����
#                         format='%(asctime)s - %(levelname)s - %(message)s',
#                         filename='weather.txt',
#                         filemode='w')
#     df = pd.read_csv(r'C:\Users\Administrator\PycharmProjects\pythonProject\weather\areaCode.csv',encoding='gbk')
#     province_df = df.query('exclude > 0').query('areacode < 101080902')
#
#     for i in province_df['areacode']:
#         logging.info('���б���:'+str(i))
#         weather_request(i)
import pandas as pd

# ����ʾ��DataFrame
data = {'A': [1, 2, 3],
        'B': [4, 5, 6],
        'C': [7, 8, 9]}
df = pd.DataFrame(data)

# ָ���µ���˳��
new_order = ['B', 'A', 'C']

# ʹ��reindex()��������������
df = df.reindex(columns=new_order)

# ��ӡ�޸ĺ��DataFrame
print(df)
