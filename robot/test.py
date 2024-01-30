from yssdk.dli.sql_client import YsDliSQLCLient
from yssdk.common.printter import Printter
from yssdk.common.alarm import Alarm
import datetime
import time
import sys
import argparse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_timestamp():
    now_time = datetime.datetime.now()

    today = now_time.strftime("%Y%m%d") + "07"
    yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y%m%d") + "07"

    end_timestamp = int(time.mktime(time.strptime(today, '%Y%m%d%H')))
    start_timestamp = int(time.mktime(time.strptime(yesterday, '%Y%m%d%H')))
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y%m%d")

    Printter.info('start_timestamp:{}, end_timestamp:{}'.format(start_timestamp, end_timestamp))
    return start_timestamp, end_timestamp, yesterday, today, tomorrow


def check_consistency():
    dli_client.exec_sql(dli_sql)
    dli_result = dli_client.fetch_all()

    count_amount = 0
    for line in dli_result:
        count_amount = line[1] + count_amount
    match = count_amount >= 200000
    if match is True:
        alarm.set_color("green")
        print(alarm.alarm_content)
        alarm.set_alarm_desc('商品库_商品动销得分 正确')
        print(alarm.alarm_content)
        for line in dli_result:
            alarm.set_alarm_field(line[0], f'{line[1]}款')
        alarm.set_alarm_field('共有商品款', f'{count_amount}款')
        alarm.set_alarm_field('告警作业所在空间', 'yishou_daily')
        alarm.set_alarm_field('告警作业名', '商品动销得分')
        alarm.set_alarm_field('DLI的SQL语句', dli_sql)
        alarm.set_alarm_url('https://open.feishu.cn/open-apis/bot/v2/hook/c4c36050-d785-4765-91ed-0176ba819bba')
        alarm.send_to_feishu(alarm.build_alarm())
        sys.exit(0)
    else:
        alarm.set_color("red")
        alarm.set_alarm_desc('商品库_商品动销商品款小于20万')
        alarm.set_alarm_field('告警作业所在空间', 'yishou_daily')
        alarm.set_alarm_field('告警作业名', '商品动销得分')
        alarm.set_alarm_field('DLI的SQL语句', dli_sql)
        alarm.set_alarm_field('检查结果', f'商品库_商品动销商品小于20万,只有[{count_amount}]款')
        alarm.set_alarm_url('https://open.feishu.cn/open-apis/bot/v2/hook/c4c36050-d785-4765-91ed-0176ba819bba')
        alarm.send_to_feishu(alarm.build_alarm())
        sys.exit(1)


if __name__ == '__main__':
    # 获取开始时间和结束时间
    start_timestamp, end_timestamp, start_day, end_day, tomorrow = get_timestamp()
    # check_period = '%s 至 %s'%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_timestamp)),time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_timestamp)))

    dli_client = YsDliSQLCLient()

    alarm = Alarm(alarm_title=f'检查当前商品库_商品动销得分,商品款分布情况')

    dli_sql = "select goods_level,count(1) from yishou_daily.dtl_goods_score_level where goods_level ='S' group by goods_level union all select * from (select goods_level,count(1) from yishou_daily.dtl_goods_score_level where goods_level !='S' group by goods_level order by goods_level asc)"
    Printter.info('DLI 查询语句:%s' % dli_sql)

    check_consistency()
