from yssdk.dli.sql_client import YsDliSQLCLient
from yssdk.common.printter import Printter
from yssdk.common.alarm import Alarm
import datetime
import time
import sys
import argparse
import urllib3

if __name__ == '__main__':
    Dli = YsDliSQLCLient()
    alarm = Alarm(alarm_title='离线因子')
    sql = 'SELECT count(supply_id),sum(seven_real_gmv),sum(seven_big_users_pay) FROM yishou_recommendation_system.dtl_supply_factor_offline'
    Dli.exec_sql(sql)
    result = Dli.fetch_all()
    if int(result[0][0]) > 3000:
        alarm.set_color('green')
        alarm.set_alarm_desc('告警口径')
        alarm.set_alarm_field('supply_id_cnt', result[0][0])
        alarm.set_alarm_field('real_gmv_sum', result[0][1])
        alarm.set_alarm_field('big_user_sum', result[0][2])
        alarm.set_alarm_url('https://open.feishu.cn/open-apis/bot/v2/hook/4361258d-c97b-4f14-9f24-1891d0f27d5a')
        alarm.send_to_feishu(alarm.build_alarm())
