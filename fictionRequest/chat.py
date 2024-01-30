## PYTHON
## ******************************************************************** ##
## author: lizhenjiang
## create time: 2022/09/27 15:35:03 GMT+08:00
## ******************************************************************** ##
'''
生成ODS作业
参数：
-m mysql的库名
-t mysql的表名

如：-m yishou_flask -t fmys_goods_ext
'''

from yssdk.mysql.client import YsMysqlClient
from yssdk.dgc.client import YsDgcClient
from yssdk.common.printter import Printter
from yssdk.common.config import Config
import pandas as pd
import argparse
import json
import string


def get_mysql_table_column(mysql_db, mysql_table):
    '''
    获取mysql的字段信息
    '''
    sql_column_desc = "select COLUMN_NAME,DATA_TYPE,COLUMN_COMMENT,COLUMN_KEY from information_schema.COLUMNS where TABLE_SCHEMA = '%s' and TABLE_NAME='%s'" % (
    mysql_db, mysql_table)
    column_desc_header = ['field_name', 'field_type', 'field_comment', 'key']
    column_desc = mysql_client.select(sql=sql_column_desc)
    df = pd.DataFrame(list(column_desc), columns=column_desc_header)
    fields = df.sort_values('field_name').to_dict(orient='records')
    return fields


def get_table_primary_key(mysql_db, mysql_table):
    '''
    获取主键
    '''
    sql_primary_key = "select COLUMN_NAME from information_schema.COLUMNS where TABLE_SCHEMA = '%s' and TABLE_NAME='%s' and COLUMN_KEY = 'PRI'" % (
    mysql_db, mysql_table)
    primary_key = []
    pk_return = mysql_client.select(sql=sql_primary_key)
    for pk in pk_return:
        primary_key.append(pk[0])
    primary_keys = ",".join(primary_key)
    return primary_keys


def generate_binlog_today_query(mysql_db, mysql_table):
    '''
    生成今天增量数据的select语句
    '''
    fields = get_mysql_table_column(mysql_db, mysql_table)
    today_sql = 'select \n'
    for field in fields:
        # print(field)
        column = field['field_name']
        today_sql += "get_json_object(columns ,'$.%s.value') as %s\n" % (column, column)
        today_sql += ","

    today_sql += "nano_time as nano_time\n"
    today_sql += ",event as event\n"
    today_sql += "from ^-^{yishou_data_dbname}.ods_binlog_data\n"
    today_sql += "where dt >= ^-^{today} and tb = '%s'" % (mysql_table)
    return today_sql


def generate_binlog_one_day_ago_query(mysql_db, mysql_table):
    '''
    生成昨天增量数据的select语句
    '''

    bodaq_sql = generate_binlog_today_query(mysql_db, mysql_table).replace('today', 'one_day_ago')
    return bodaq_sql


def generate_one_day_ago_query(mysql_db, mysql_table):
    '''
    生成1天前历史数据的select 语句
    '''
    fields = get_mysql_table_column(mysql_db, mysql_table)
    ods_table = 'ods_%s_dt' % (mysql_table)
    odaq_sql = 'select \n'
    for field in fields:
        column = field['field_name']
        odaq_sql += "%s\n" % column
        odaq_sql += ","

    odaq_sql += "-987654321012345 as nano_time\n"
    odaq_sql += ",0 as event\n"
    odaq_sql += "from ^-^{yishou_data_dbname}.%s\n" % (ods_table)
    odaq_sql += "where dt = ^-^{one_day_ago}"
    return odaq_sql


def generate_two_day_ago_query(mysql_db, mysql_table):
    '''
    生成2天前历史数据的select 语句
    '''
    tdaq = generate_one_day_ago_query(mysql_db, mysql_table).replace('one_day_ago', 'two_day_ago')
    return tdaq


def generate_union_query(mysql_db, mysql_table):
    '''
    生成历史和增量数据union all 语句
    '''
    union_sql = ''
    if table_type == 'view':
        union_sql += generate_one_day_ago_query(mysql_db, mysql_table)
        union_sql += '\n'
        union_sql += 'union all'
        union_sql += '\n'
        union_sql += generate_binlog_today_query(mysql_db, mysql_table)
    else:
        union_sql += generate_two_day_ago_query(mysql_db, mysql_table)
        union_sql += '\n'
        union_sql += 'union all'
        union_sql += '\n'
        union_sql += generate_binlog_one_day_ago_query(mysql_db, mysql_table)
    return union_sql


def generate_row_number_query(mysql_db, mysql_table):
    '''
    生成row_number()排序语句
    '''
    fields = get_mysql_table_column(mysql_db, mysql_table)
    primary_keys = get_table_primary_key(mysql_db, mysql_table)
    dep_sql = 'select \n'
    for field in fields:
        column = field['field_name']
        dep_sql += '%s\n' % (column)
        dep_sql += ','
    dep_sql += 'nano_time\n'
    dep_sql += ',event\n'
    dep_sql += ',row_number() over(partition by %s order by nano_time desc) as row_number\n' % (primary_keys)
    dep_sql += 'from ( \n'
    dep_sql += generate_union_query(mysql_db, mysql_table)
    dep_sql += '\n)\n'
    return dep_sql


def generate_insert(mysql_db, mysql_table):
    '''
    生成ods表的insert overwrite语句
    '''
    fields = get_mysql_table_column(mysql_db, mysql_table)
    ods_table = 'ods_%s_dt' % (mysql_table)
    insert_sql = '\ninsert overwrite table ^-^{yishou_data_dbname}.%s partition(dt)\n' % (ods_table)
    insert_sql += 'select\n'
    for field in fields:
        column = field['field_name']
        insert_sql += '%s\n' % (column)
        insert_sql += ','
    insert_sql += '^-^{one_day_ago} as dt\n'
    insert_sql += 'from (\n'
    insert_sql += generate_row_number_query(mysql_db, mysql_table)
    insert_sql += ')\n'
    insert_sql += 'where row_number = 1 and event != 1\n'
    insert_sql += 'DISTRIBUTE BY floor(rand()*50)'
    return insert_sql


def generate_view(mysql_db, mysql_table):
    '''
    生成视图创建语句
    '''
    fields = get_mysql_table_column(mysql_db, mysql_table)
    view_name = 'ods_%s_view' % (mysql_table)
    view_sql = '\ndrop view if exists ^-^{yishou_data_dbname}.%s;\n' % (view_name)
    view_sql += 'create view if not exists ^-^{yishou_data_dbname}.%s(\n' % (view_name)
    fields_num = len(fields)
    for field in fields:
        column = field['field_name']
        view_sql += '%s\n' % (column)
        fields_num -= 1
        if fields_num > 0:
            view_sql += ','
    view_sql += ')\n'
    view_sql += "comment '%s在ods层视图（根据业务库数据，分钟级别更新）'\n" % (mysql_table)
    view_sql += 'as \n'
    view_sql += 'select \n'
    fields_num = len(fields)
    for field in fields:
        column = field['field_name']
        view_sql += '%s\n' % (column)
        fields_num -= 1
        if fields_num > 0:
            view_sql += ','
    view_sql += 'from (\n'
    view_sql += generate_row_number_query(mysql_db, mysql_table)
    view_sql += ')\n'
    view_sql += 'where row_number = 1 and event != 1'
    return view_sql


def create_script(setting):
    '''
    创建DGC脚本
    '''
    resp = ys_dgc_client.create_script(method='POST',
                                       url=url,
                                       workspace_name='yishou_data',
                                       body=json.dumps(setting))
    print(resp.status_code, resp.content)


def create_job(workspace_name):
    '''
    创建DGC作业,如果存在则提交新的版本
    '''

    # 作业参数
    dgc_job_parameters = {
        'mysql_table_name': mysql_table,
        'dli_table_name': ods_table,
        'dli_view_name': view_name,
        'view_sql': view_sql,
        'insert_sql': insert_sql
    }

    job_exists = ys_dgc_client.check_job_exists(method='GET',
                                                url='%s?jobName=%s' % (job_url, ods_table),
                                                workspace_name=workspace_name)

    if job_exists is False:
        # 作业不存在,创建
        Printter.info('作业不存在,创建')
        job_setting = ys_dgc_client.generate_dgc_job_setting(parameters=dgc_job_parameters,
                                                             template_file='template_ods.json')
        resp = ys_dgc_client.create_job(method='POST',
                                        url=job_url,
                                        workspace_name=workspace_name,
                                        body=job_setting)

    else:
        # 作业已存在,提交新的版本
        Printter.info('作业已存在,提交新的版')
        job_setting = ys_dgc_client.generate_dgc_job_setting(parameters=dgc_job_parameters,
                                                             template_file='template_ods.json')
        resp = ys_dgc_client.create_job(method='PUT',
                                        url='%s/%s' % (job_url, ods_table),
                                        workspace_name=workspace_name,
                                        body=job_setting)

    return_code = '返回代码:%d' % (resp.status_code)
    if resp.status_code == 204:
        Printter.info(str(return_code), '执行成功')
    else:
        Printter.error('执行失败')
        Printter.error(return_code, resp.content.decode())


def update_binlog_configure_center(table_name, primary_column, queue='analyst_queue'):
    '''
    在配置中心新增binlog配置
    '''

    mysql_client = YsMysqlClient()
    mysql_client.get_zzconnect()
    insert_template = "insert into data_center.register_schema set \
            topic ='bigdata_mysql_binlog_avro',\
            business_table_name ='${table_name}',\
            primary_column ='${primary_column}',\
            binlog_type ='2',\
            create_time = now(),\
            quene ='${queue}'"

    insert_template_sql = string.Template(insert_template)
    insert_sql = insert_template_sql.safe_substitute(table_name=table_name, primary_column=primary_column, queue=queue)
    check_sql = "select * from data_center.register_schema where business_table_name ='%s'" % table_name
    Printter.info('在配置中心新增binlog配置：%s' % table_name)
    if len(mysql_client.select(check_sql, None)) == 0:
        mysql_client.update(sql=insert_sql)
    else:
        Printter.info('配置已存在，跳过')


if __name__ == '__main__':
    # 获取参数
    # parser = argparse.ArgumentParser(description='ArgUtils')
    # parser.add_argument('-m', type=str, default=None, help="mysql库名")
    # parser.add_argument('-t', type=str, default=None, help="mysql表名")
    #
    # args = parser.parse_args()

    # mysql_db = args.m
    # mysql_table = args.t
    mysql_db = 'yishou_flask'
    mysql_table = 'fmys_goods_feedback'

    Printter.info("mysql库名: [%s]" % mysql_db)
    Printter.info("mysql表名: [%s]" % mysql_table)

    ods_table = 'ods_%s_dt' % (mysql_table)
    view_name = 'ods_%s_view' % (mysql_table)
    mysql_client = YsMysqlClient()
    mysql_client.get_r7connect()
    ys_dgc_client = YsDgcClient()
    conf = Config.get_config()
    job_url = conf['dgc_conf']['job_url']

    # 生成insert语句
    table_type = 'insert'
    insert_sql = generate_insert(mysql_db, mysql_table).replace('^-^', '$')

    # 生成view语句
    table_type = 'view'
    view_sql = generate_view(mysql_db, mysql_table).replace('^-^', '$')

    # 创建DGC作业
    create_job('yishou_data')

    # 配置中心, 添加binlog配置
    table_name = '%s.%s' % (mysql_db, mysql_table)
    primary_keys = get_table_primary_key(mysql_db, mysql_table)
    update_binlog_configure_center(table_name=table_name, primary_column=primary_keys)

