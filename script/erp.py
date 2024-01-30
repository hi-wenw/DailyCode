# -*- coding: utf8 -*-
import re

import pandas
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = 'http://erp10.yishou.com/xdebug/index/create_sql'

    response = requests.get(url)

    response.encoding = 'utf8'

    soup = BeautifulSoup(response.text, 'lxml')

    result = soup.find_all('div', class_='pretty')

    ls = []
    for sql in result:
        createSQL = sql.text

        # 解析表名
        table_name_pattern = re.compile(r"CREATE\s+TABLE\s+`(\w+)`")
        table_name_match = table_name_pattern.search(createSQL)
        table_name = table_name_match.group(1)

        # 解析字段名和注释
        fields_pattern = re.compile(r"`(\w+)`\s+(\w+)\s+.*COMMENT\s+'(.*)'")
        fields_matches = fields_pattern.findall(createSQL)

        # 输出结果
        for field in fields_matches:
            field_name = field[0]
            field_type = field[1]
            field_comment = field[2]
            print(f"表名：{table_name}，字段名：{field_name}，类型：{field_type}，注释：{field_comment}")

            ls.append([table_name, field_name, field_type, field_comment])

    df = pandas.DataFrame(ls, columns=['table_name', 'field_name', 'field_type', 'comment'])

    df.to_csv('erp_Data.csv', index=False)
