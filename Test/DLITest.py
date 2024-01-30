from yssdk.dli.sql_client import YsDliSQLCLient

if __name__ == '__main__':
    client = YsDliSQLCLient()
    YsDliSQLCLient(conf_mode='dev')     # 本地开发测试时使用参数conf_mode='dev'
    sql = 'show databases;'

    client.exec_sql(sql)
    print(client.fetch_all())