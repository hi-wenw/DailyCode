# -*- coding: utf-8 -*-

import time
from datetime import datetime

import redis

r = redis.Redis(host='139.159.134.78', port=16379, db=0, password='m6ojIOg1rvcc5go8')
pip = r.pipeline()

user_id = 8828091
third_cat_id = 299


def recommendation_category(user_id, third_cat_id):  # put application's code here
    # return jsonify([])
    interface_start_time = datetime.now()
    # 配置信息
    # RECOMMEND_TOP_N = app.config.get('RECOMMEND_TOP_N')
    # REDIS_RECALL_NUM = app.config.get('REDIS_RECALL_NUM')
    REDIS_RECALL_NUM = 600
    pip = redis.Redis(host='139.159.134.78', port=16379, db=0, password='m6ojIOg1rvcc5go8').pipeline()
    redis_key = str(user_id) + "_" + str(third_cat_id)  # 组合键

    # 1.1redis批量获取数据
    resp = {}
    redis_start_time = time.time()

    pip.hget('classify_recall_for_als', redis_key)
    pip.hget('classify_recall_for_tag', redis_key)
    pip.hget('classify_recall_for_hot', redis_key)
    pip.hget('goods_similar', redis_key)  # 相似商品召回策略1
    pip.hget('new_goods_similar', redis_key)  # 相似商品召回策略2
    pip.hget('classify_recall_for_bpr_cf', redis_key)
    pip.hget('classify_recall_for_user_similar_rec', redis_key)
    results = pip.execute()
    redis_end_time = time.time()
    # app.logger.debug(f'[{user_id}],[{third_cat_id}] redis查询时间：[{redis_end_time - redis_start_time}]')
    print(results)
    # 1.2 判断数据是否为空
    if all(result is None or result == b'' for result in results):
        resp['total'] = 0
        resp['goods_recommend'] = []
        # app.logger.info(f'接口执行时间：{datetime.now() - interface_start_time}，user_id：{user_id}，keyword：{keyword}')
        return resp

    # 1.3生成货号列表(每个策略比例一致)
    goods_no_list = []
    avg_recall_num = REDIS_RECALL_NUM // len(results) - 1

    for result in results:
        if result:
            print(len(result.decode('utf-8').split(',')))
            product_ids = result.decode('utf-8').split(',')[:avg_recall_num]
            goods_no_list.extend(product_ids)
    print(goods_no_list)
    goods_no_len = len(goods_no_list)
    goods_no_str = ','.join(goods_no_list)
    goods_no_tuple = eval(goods_no_str)
    print(len(goods_no_list))


if __name__ == '__main__':
    # recommendation_category(8828091, 299)
    strategy_list = ['classify_recall_for_als', 'classify_recall_for_tag', 'classify_recall_for_hot', 'goods_similar',
                     'new_goods_similar', 'classify_recall_for_bpr_cf', 'classify_recall_for_user_similar_rec']
    strategy_dict = {}
    for strategy in strategy_list:
        strategy_dict[strategy] = r.hget('recall_ratio', strategy.upper() + '_RECALL_RATIO')

    print(strategy_dict)
    # print(type(recall_ratio))
    # for i in recall_ratio:
    #     print(600*float(i.decode('utf8')))

    # set()列表去重
    list1 = ['a', 'b', 1, 3, 9, 9, 'a']
    list2 = list(set(list1))
    print(list2)
