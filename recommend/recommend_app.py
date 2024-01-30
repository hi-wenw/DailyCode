# 分品类推荐项目接口你
import json
import time

import pymysql
from dbutils.pooled_db import PooledDB
from psycopg2.extras import DictCursor
from pymysql import converters, FIELD_TYPE
import redis
from flask import Flask, Blueprint, jsonify
def weighted_sum_rerank_v1(goods_ls, goods_similar_score_dict, goods_behavior_type_dict, goods_ctr_dict,
                           goods_pay_rate_dict, top_k=100):
    # goods_score_dict={}
    # for i in np.arange(len(goods_ls)):
    #     for j in np.arange(len(goods_ls[i])):
    #         good_no = goods_ls[i][j]
    #         good_similar_score = goods_score_ls[i][j]
    #         if good_no  in goods_score_dict.keys() and good_similar_score>goods_score_dict[good_no]:
    #             goods_score_dict[good_no]=good_similar_score
    #         elif good_no not in goods_score_dict.keys():
    #             goods_score_dict[good_no] = good_similar_score

    # goods_score_ls=[]

    # for goods in goods_score_dict.keys():
    #     if goods_uv_value_dict == {}:
    #         goods_score_dict[goods] = goods_score_dict[goods]
    #     else:
    #         goods_score_dict[goods]=goods_score_dict[goods]*goods_uv_value_dict[goods]
    #
    #     goods_score_ls.append([goods,
    #                            goods_score_dict[goods]
    #                            ])

    # 根据MYSQL过滤商品
    goods_filter_ls = goods_ls
    # goods_filter_ls = [goods_no for goods_no in goods_ls if goods_no in goods_ctr_dict.keys()]

    goods_score_ls = []
    for good_no in goods_filter_ls:
        similar_score = 0
        behavior_score = 0
        ctr_score = 0
        pay_rate = 0

        if good_no not in goods_ctr_dict.keys():
            continue

        if good_no in goods_similar_score_dict.keys() and goods_similar_score_dict[good_no] is not None:
            similar_score = goods_similar_score_dict[good_no]
        '''
        if good_no in goods_behavior_type_dict.keys():
            if goods_behavior_type_dict[good_no] == 'cart_or_order':
                behavior_score = 0.7
            elif goods_behavior_type_dict[good_no] == 'click':
                behavior_score = 0.3
        if good_no in goods_ctr_dict.keys() and goods_ctr_dict[good_no] is not None:
            ctr_score = goods_ctr_dict[good_no]
        '''
        if good_no in goods_pay_rate_dict.keys() and goods_pay_rate_dict[good_no] is not None:
            pay_rate = goods_pay_rate_dict[good_no]
            # if pay_rate == 0:
            #     pay_rate = -0.35
        # if pay_rate == 0:
        #     pay_rate = -0.05  # -0.02#-0.5 #5
        #     score = similar_score + pay_rate
        # else:
        #     score = similar_score+pay_rate*0.2  # 0.5

        if pay_rate == 0:
            pay_rate = -0.35  # -0.35  # -0.02#-0.5 #5

        if similar_score >= 0.75 and pay_rate > 0:
            score = 0.7 + pay_rate
        elif similar_score >= 0.55 and similar_score < 0.75 and pay_rate > 0:
            score = similar_score * 0.5 + pay_rate
        elif similar_score >= 0.75 and pay_rate < 0:
            score = similar_score + pay_rate
        else:
            score = pay_rate

            # if not str(ctr_score).isdigit(): #
        #     ctr_score = 0
        # if not str(pay_rate).isdigit():
        #     pay_rate = 0

        # score = similar_score / 3 + behavior_score / 3 + ctr_score * 0.8 / 3 + pay_rate * 0.2 / 3
        # score = similar_score+pay_rate#*10#*100

        goods_score_ls.append([good_no, score])

    goods_score_ls = sorted(goods_score_ls, key=lambda x: x[1], reverse=True)

    rec_goods_ls = [i[0] for i in goods_score_ls[0:top_k]]

    return rec_goods_ls

class BasePymysqlPool(object):
    def __init__(self, host, port, user, password, db_name=None):
        self.conv = converters.conversions
        self.conv[FIELD_TYPE.NEWDECIMAL] = float  # convert decimals to float
        self.conv[FIELD_TYPE.DATE] = str  # convert dates to strings
        self.conv[FIELD_TYPE.TIMESTAMP] = str  # convert dates to strings
        self.conv[FIELD_TYPE.DATETIME] = str  # convert dates to strings
        self.conv[FIELD_TYPE.TIME] = str  # convert dates to strings
        self.db_host = host
        self.db_port = int(port)
        self.user = user
        self.password = str(password)
        self.db = db_name
        self.conn = None
        self.cursor = None

class MysqlPool(BasePymysqlPool):
    """
    MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现获取连接对象：conn = Mysql.getConn()
            释放连接对象;conn.close()或del conn
    """
    # 连接池对象
    __pool = None

    def __init__(self, host, port, user, password, db_name):
        super(MysqlPool, self).__init__(host, port, user, password, db_name)
        # 数据库构造函数，从连接池中取出连接，并生成操作游标

    def __getConn(self):
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection

        charset = 'utf8', use_unicode = True
        """
        if MysqlPool.__pool is None:
            MysqlPool.__pool = PooledDB(creator=pymysql,
                                        mincached=1,
                                        maxcached=2000,
                                        host=self.db_host,
                                        port=self.db_port,
                                        maxconnections=2000,
                                        user=self.user,
                                        passwd=self.password,
                                        db=self.db,
                                        use_unicode=True,
                                        charset="utf8",
                                        blocking=True,
                                        conv=self.conv,
                                        cursorclass=DictCursor)
        return MysqlPool.__pool.connection()

app = Flask(__name__)
app.config.from_pyfile('settings.py')

mysql_pool = MysqlPool(app.config.get('MYSQL_HOST')
                       , app.config.get('MYSQL_PORT')
                       , app.config.get('MYSQL_USER')
                       , app.config.get('MYSQL_PASSWORD')
                       , app.config.get('MYSQL_DB_NAME')
                       )
top_k = app.config.get("TOP_K")

main = Blueprint('main', __name__, template_folder='templates')
app.register_blueprint(main)
@main.route('/recommendation/<int:user_id>/<int:third_cat_id>', methods=['GET'])
# @app.errorhandler(werkzeug.exceptions.BadRequest)
def recommendation_category(user_id, third_cat_id):  # put application's code here
    # return jsonify([])

    # redis批量获取数据
    redis_start_time = time.time()
    pip = redis.Redis(connection_pool=redis_pool).pipeline()
    redis_key = str(user_id) + "_" + str(third_cat_id)
    pip.hget('user_cat_goods_order', redis_key)
    pip.hget('user_cat_goods_add_cart', redis_key)
    pip.hget('user_cat_goods_click', redis_key)
    pip.hget('goods_recommend_exposure_suppress', redis_key)
    results = pip.execute()
    redis_end_time = time.time()
    app.logger.debug(f'[{user_id}],[{third_cat_id}] redis查询时间：[{redis_end_time - redis_start_time }]')

    # 购买排序
    order_add_carts = []
    order_add_cart_limit = 5  # 7  # 10
    if results[0] is not None:
        order_behaviors_json = json.loads(results[0])
        order_event_times = order_behaviors_json.get('event_time_list').split('_')
        order_goods_no_lists = order_behaviors_json.get('goods_no_list').split('_')
        for index in range(len(order_goods_no_lists)):
            if order_goods_no_lists[index] != '' and order_goods_no_lists[index] != '':
                order_add_carts.append((
                    int(order_goods_no_lists[index]),
                    'order',
                    int(order_event_times[index])
                ))
    app.logger.debug('购买排序')

    # 加购排序
    if results[1] is not None:
        add_cart_behaviors = json.loads(results[1])
        add_cart_event_times = add_cart_behaviors.get('event_time_list').split('_')
        add_cart_goods_no_lists = add_cart_behaviors.get('goods_no_list').split('_')
        for index in range(len(add_cart_goods_no_lists)):
            find = False
            for jndex in range(len(add_cart_goods_no_lists)):
                if int(add_cart_goods_no_lists[index]) == int(add_cart_goods_no_lists[jndex]):
                    find = True
                    break
            if not find:
                order_add_carts.append((
                    int(add_cart_goods_no_lists[index]),
                    'add_cart',
                    int(add_cart_event_times[index])
                ))
    app.logger.debug('加购排序')
    order_add_carts = sorted(order_add_carts, key=lambda t: t[2], reverse=True)
    if len(order_add_carts) > order_add_cart_limit:
        order_add_carts = order_add_carts[0:order_add_cart_limit]

    # 点击排序
    click_num_limit = 5  # 7  # 5  # 10
    clicks = []
    if results[2] is not None:
        click_behaviors_json = json.loads(results[2])
        click_event_times = click_behaviors_json.get('event_time_list').split('_')
        click_goods_no_lists = click_behaviors_json.get('goods_no_list').split('_')
        for index in range(len(click_goods_no_lists)):
            find = False
            for jndex in range(len(order_add_carts)):
                if int(click_goods_no_lists[index]) == order_add_carts[jndex][0]:
                    find = True
                    break
            if not find:
                clicks.append((
                    int(click_goods_no_lists[index]),
                    'click',
                    int(click_event_times[index])
                ))
    clicks = sorted(clicks, key=lambda t: t[2], reverse=True)
    if len(clicks) > click_num_limit:
        clicks = clicks[0:click_num_limit]
    app.logger.debug('完成点击查询')
    export_goods_nos = []
    # 曝光打压
    if results[3] is not None:
        export_goods_nos = results[3].split(', ')

    app.logger.debug('曝光打压')
    sort_end_time = time.time()
    app.logger.debug(f'[{user_id}],[{third_cat_id}]  排序时间:[{sort_end_time - redis_end_time}]')

    similar_goods_ls, similar_score_dict, similar_goods_behavior_type_dict = similar.query_similar_goods(clicks,order_add_carts,export_goods_nos,top_k)

    model_end_time = time.time()
    app.logger.debug(f'[{user_id}],[{third_cat_id}]  similar模型调用时间:[{model_end_time - sort_end_time}]')

    goods_ctr_dict = {}
    goods_pay_rate_dict = {}
    if len(similar_goods_ls) > 0:
        goods_no_str = ''
        for goods_no in similar_goods_ls:
            goods_no_str = goods_no_str + str(goods_no) + ','
        goods_no_str = goods_no_str[0:len(goods_no_str) - 1]
        sql = f"select goods_no, exposure_click_rate_3day, uv_value_3day as exposure_pay_rate_3day2 from goods_recommend_goods_profile where 1=1 and goods_no in({goods_no_str}) and cat_id = {third_cat_id}"
        mysql_start_time = time.time()
        rs = mysql_pool.getAll(sql)
        app.logger.debug('完成Mysql查询')
        mysql_end_time = time.time()
        cha_value = mysql_end_time - mysql_start_time
        app.logger.debug(f'[{user_id}],[{third_cat_id}]  mysql查询时间:[{cha_value}]')
        if cha_value > 0.1:
            app.logger.debug(f'执行的sql为：[{sql}]')
        if rs is not None:
            for line in rs:
                goods_ctr_dict[line.get('goods_no')] = line.get('exposure_click_rate_3day')
                goods_pay_rate_dict[line.get('goods_no')] = line.get('exposure_pay_rate_3day2')

        goods_no_list = weighted_sum_rerank_v1(similar_goods_ls, similar_score_dict,
                                               similar_goods_behavior_type_dict,
                                               goods_ctr_dict, goods_pay_rate_dict, top_k)
        rerank_model = time.time()
        app.logger.debug(f'[{user_id}],[{third_cat_id}]  rerank模型调用时间:[{rerank_model - mysql_end_time}]')
        app.logger.info(f'有数据模型统计:[{user_id}]|[{third_cat_id}]|[{len(goods_no_list)}]')
        return jsonify(goods_no_list)
    else:
        app.logger.info(f'无数据模型统计:[{user_id}]|[{third_cat_id}]')
        return jsonify([])