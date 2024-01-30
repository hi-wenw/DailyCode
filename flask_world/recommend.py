from flask import Blueprint
from config.goods_sqls import goods_sql
import jieba
# ����route
""" ��ʼ���� """
# controller�����࣬main����Ҫ����controller�ĳ�ʼ�����ϣ���Ȼcontroller�����ʼ��
main = Blueprint('main', __name__, template_folder='templates')

import json

import redis
from flask import jsonify
from itertools import zip_longest

#from models.recall.similar_goods_base_goods_emb_recall import Similar4OldGood
from models.rerank.similar_goods_rerank import weighted_sum_rerank_v1
from services.init import redis_pool, similar, top_k, mysql_pool, load_models, model_pool, obsClient
from recommend_app import app
import time
from datetime import datetime, timedelta
from flask import request

import numpy as np
from numpy import append
from datetime import datetime
from services.services import fetch_es_data
import traceback


# ��Ʒ���Ƽ���Ŀ�ӿ���
@main.route('/recommendation/<int:user_id>/<int:third_cat_id>', methods=['GET'])
# @app.errorhandler(werkzeug.exceptions.BadRequest)
def recommendation_category(user_id, third_cat_id):  # put application's code here
    return jsonify([])

    # redis������ȡ����
    # redis_start_time = time.time()
    # pip = redis.Redis(connection_pool=redis_pool).pipeline()
    # redis_key = str(user_id) + "_" + str(third_cat_id)
    # pip.hget('user_cat_goods_order', redis_key)
    # pip.hget('user_cat_goods_add_cart', redis_key)
    # pip.hget('user_cat_goods_click', redis_key)
    # pip.hget('goods_recommend_exposure_suppress', redis_key)
    # results = pip.execute()
    # redis_end_time = time.time()
    # app.logger.debug(f'[{user_id}],[{third_cat_id}] redis��ѯʱ�䣺[{redis_end_time - redis_start_time }]')
    #
    # # ��������
    # order_add_carts = []
    # order_add_cart_limit = 5  # 7  # 10
    # if results[0] is not None:
    #     order_behaviors_json = json.loads(results[0])
    #     order_event_times = order_behaviors_json.get('event_time_list').split('_')
    #     order_goods_no_lists = order_behaviors_json.get('goods_no_list').split('_')
    #     for index in range(len(order_goods_no_lists)):
    #         if order_goods_no_lists[index] != '' and order_goods_no_lists[index] != '':
    #             order_add_carts.append((
    #                 int(order_goods_no_lists[index]),
    #                 'order',
    #                 int(order_event_times[index])
    #             ))
    # app.logger.debug('��������')
    #
    # # �ӹ�����
    # if results[1] is not None:
    #     add_cart_behaviors = json.loads(results[1])
    #     add_cart_event_times = add_cart_behaviors.get('event_time_list').split('_')
    #     add_cart_goods_no_lists = add_cart_behaviors.get('goods_no_list').split('_')
    #     for index in range(len(add_cart_goods_no_lists)):
    #         find = False
    #         for jndex in range(len(add_cart_goods_no_lists)):
    #             if int(add_cart_goods_no_lists[index]) == int(add_cart_goods_no_lists[jndex]):
    #                 find = True
    #                 break
    #         if not find:
    #             order_add_carts.append((
    #                 int(add_cart_goods_no_lists[index]),
    #                 'add_cart',
    #                 int(add_cart_event_times[index])
    #             ))
    # app.logger.debug('�ӹ�����')
    # order_add_carts = sorted(order_add_carts, key=lambda t: t[2], reverse=True)
    # if len(order_add_carts) > order_add_cart_limit:
    #     order_add_carts = order_add_carts[0:order_add_cart_limit]
    #
    # # �������
    # click_num_limit = 5  # 7  # 5  # 10
    # clicks = []
    # if results[2] is not None:
    #     click_behaviors_json = json.loads(results[2])
    #     click_event_times = click_behaviors_json.get('event_time_list').split('_')
    #     click_goods_no_lists = click_behaviors_json.get('goods_no_list').split('_')
    #     for index in range(len(click_goods_no_lists)):
    #         find = False
    #         for jndex in range(len(order_add_carts)):
    #             if int(click_goods_no_lists[index]) == order_add_carts[jndex][0]:
    #                 find = True
    #                 break
    #         if not find:
    #             clicks.append((
    #                 int(click_goods_no_lists[index]),
    #                 'click',
    #                 int(click_event_times[index])
    #             ))
    # clicks = sorted(clicks, key=lambda t: t[2], reverse=True)
    # if len(clicks) > click_num_limit:
    #     clicks = clicks[0:click_num_limit]
    # app.logger.debug('��ɵ����ѯ')
    # export_goods_nos = []
    # # �ع��ѹ
    # if results[3] is not None:
    #     export_goods_nos = results[3].split(', ')
    #
    # app.logger.debug('�ع��ѹ')
    # sort_end_time = time.time()
    # app.logger.debug(f'[{user_id}],[{third_cat_id}]  ����ʱ��:[{sort_end_time - redis_end_time}]')
    #
    # similar_goods_ls, similar_score_dict, similar_goods_behavior_type_dict = similar.query_similar_goods(clicks,order_add_carts,export_goods_nos,top_k)
    #
    # model_end_time = time.time()
    # app.logger.debug(f'[{user_id}],[{third_cat_id}]  similarģ�͵���ʱ��:[{model_end_time - sort_end_time}]')
    #
    # goods_ctr_dict = {}
    # goods_pay_rate_dict = {}
    # if len(similar_goods_ls) > 0:
    #     goods_no_str = ''
    #     for goods_no in similar_goods_ls:
    #         goods_no_str = goods_no_str + str(goods_no) + ','
    #     goods_no_str = goods_no_str[0:len(goods_no_str) - 1]
    #     sql = f"select goods_no, exposure_click_rate_3day, uv_value_3day as exposure_pay_rate_3day2 from goods_recommend_goods_profile where 1=1 and goods_no in({goods_no_str}) and cat_id = {third_cat_id}"
    #     mysql_start_time = time.time()
    #     rs = mysql_pool.getAll(sql)
    #     app.logger.debug('���Mysql��ѯ')
    #     mysql_end_time = time.time()
    #     cha_value = mysql_end_time - mysql_start_time
    #     app.logger.debug(f'[{user_id}],[{third_cat_id}]  mysql��ѯʱ��:[{cha_value}]')
    #     if cha_value > 0.1:
    #         app.logger.debug(f'ִ�е�sqlΪ��[{sql}]')
    #     if rs is not None:
    #         for line in rs:
    #             goods_ctr_dict[line.get('goods_no')] = line.get('exposure_click_rate_3day')
    #             goods_pay_rate_dict[line.get('goods_no')] = line.get('exposure_pay_rate_3day2')
    #
    #     goods_no_list = weighted_sum_rerank_v1(similar_goods_ls, similar_score_dict,
    #                                            similar_goods_behavior_type_dict,
    #                                            goods_ctr_dict, goods_pay_rate_dict, top_k)
    #     rerank_model = time.time()
    #     app.logger.debug(f'[{user_id}],[{third_cat_id}]  rerankģ�͵���ʱ��:[{rerank_model - mysql_end_time}]')
    #     app.logger.info(f'������ģ��ͳ��:[{user_id}]|[{third_cat_id}]|[{len(goods_no_list)}]')
    #     return jsonify(goods_no_list)
    # else:
    #     app.logger.info(f'������ģ��ͳ��:[{user_id}]|[{third_cat_id}]')
    #     return jsonify([])


user_rec_label = ["����", "ʵ��"]


@main.route('/supply_recommend/<int:user_id>/<int:cat_id>/<string:scene>', methods=['GET'])
# @app.errorhandler(werkzeug.exceptions.BadRequest)
def supply_recommend(user_id, cat_id, scene):  # put application's code here

    try:
        # ��ʼ���ٻ��б�
        rec_list = []

        # ���idΪ�쳣�Ļ�ֱ�ӷ��ؿ�
        if len(model_pool.get("supply_recommend_data_load").cat_dict.get(cat_id, '')) == 0 or scene == "category":
            return jsonify({"user_id": user_id,
                            "third_cat_id": cat_id,
                            "scene": scene,
                            "rec_supply_list": []})

        cat_id_str = str(cat_id)
        rec_recson_dict = {
            "1001": {
                "search": "����" + model_pool.get("supply_recommend_data_load").cat_dict[cat_id] + "�ĵ�����ϲ����",
                "category": "����" + model_pool.get("supply_recommend_data_load").cat_dict[cat_id] + "�ĵ�������ע"},
            "1004": {
                "search": "����" + model_pool.get("supply_recommend_data_load").cat_dict[cat_id] + "�ĵ�����ϲ����",
                "category": "����" + model_pool.get("supply_recommend_data_load").cat_dict[cat_id] + "�ĵ�������ע"},
            "1002": {"search": "��������", "category": "��������"},
            "1003": {"search": "��ע���Ķ���", "category": "��ע���Ķ���"},
            "1005": {"search": "����" + model_pool.get("supply_recommend_data_load").cat_dict[cat_id] + "�ĵ���������",
                     "category": "����" + model_pool.get("supply_recommend_data_load").cat_dict[
                         cat_id] + "�ĵ���������"},
            "1006": {"search": "����" + model_pool.get("supply_recommend_data_load").cat_dict[cat_id] + "�ĵ���������",
                     "category": "����" + model_pool.get("supply_recommend_data_load").cat_dict[
                         cat_id] + "�ĵ���������"},
            "1007": {
                "search": "����" + model_pool.get("supply_recommend_data_load").cat_dict[cat_id] + "�ĵ�����ϲ����",
                "category": "����" + model_pool.get("supply_recommend_data_load").cat_dict[cat_id] + "�ĵ�������ע"}
        }
        rec_recson_random_dict = {
            "1002": {"search": 'random.choice(user_rec_label)', "category": 'random.choice(user_rec_label)'}
        }
        # ��ʼ�����õ���Эͬ�����Ƽ�����
        user_cf_buy_rec_dict = {}

        # ��ʼ��BPRЭͬ�����Ƽ�����
        user_bpr_rec_dict = {}
        pipe = redis.Redis(connection_pool=redis_pool).pipeline()
        # ��ȡ�û�����
        pipe.hget("supply_rec_user_profile", user_id)

        # ��ȡ�����û����Ƶ����Ƽ����Եĵ����Ƽ��б�
        pipe.hget("user_cf_buy_rec", user_id)

        # ��ȡЭͬ���˵����Ƽ��б�
        pipe.hget("user_bpr_rec", user_id)

        # ��ȡ�û����ع⵵���б�
        pipe.hget("supply_recommend_exposure_filter_v3", str(user_id))

        # ��ȡ�û�����������б�
        pipe.hget("supply_page_list", str(user_id))

        supply_rec_user_profile_json, user_cf_buy_rec_json, user_bpr_rec_json, user_exposure_string, user_page_string = pipe.execute()  # supply_rec_label_json,

        """��ǩ�Ƽ��߼�����"""
        # ��ȡ��ǩ�Ƽ��б�
        user_hoo_profile = 0
        json_string_hoo = json.dumps({})
        json_string_list = []
        if supply_rec_user_profile_json is not None:
            supply_rec_user_profile_dict = json.loads(supply_rec_user_profile_json)
            # ��ȡ�û�Ʒ���·�񡪵��λ���
            style_grade_dict = supply_rec_user_profile_dict.get('style_grade', {})
            user_style_grade_profile = cat_id_str + "_" + style_grade_dict.get(cat_id_str, {}).get('style', '') \
                                       + "_" + style_grade_dict.get(cat_id_str, {}).get('grade', '')

            # ��ȡ�û�Ʒ���·�񡪵���-�ݶȻ���
            style_grade_level_hoo_dict = supply_rec_user_profile_dict.get('style_grade_level_hoo', {})
            user_style_grade_level_profile = cat_id_str + "_" + style_grade_level_hoo_dict.get(cat_id_str, {}).get(
                'style',
                '') \
                                             + "_" + style_grade_level_hoo_dict.get(cat_id_str, {}).get('grade', '') \
                                             + "_" + style_grade_level_hoo_dict.get(cat_id_str, {}).get('gmv_level', '')
            # ��ȡ�û���ﻭ��
            # user_hoo_profile = style_grade_level_hoo_dict.get('Hoo', 0)

            pipe.hmget("supply_rec_label", user_style_grade_level_profile, user_style_grade_profile,
                       cat_id_str + "_���")
            pipe.hget("supply_rec_label", "���")
            json_string_list, json_string_hoo = pipe.execute()

        # if len(json_string_list) != 0:
        #     for json_string in json_string_list:
        #         if json_string is not None :
        #             rec_list.append([supply_id + "_" + json.loads(json_string)['strategy_id'] for supply_id in
        #                              json.loads(json_string)['rec_supplier_list'].split(",")])

        # 1001���Դ���
        if len(json_string_list) != 0:
            if json_string_list[0] is not None:
                tmp_rec_dict0 = json.loads(json_string_list[0])
                rec_list.append([supply_id + "_" + tmp_rec_dict0['strategy_id'] for supply_id in
                                 tmp_rec_dict0['rec_supplier_list'].split(",")])
        # Эͬ���˳��õ����Ƽ�����
        if user_cf_buy_rec_json is not None:
            user_cf_buy_rec_dict = json.loads(user_cf_buy_rec_json).get(cat_id_str, {})

        # ��������û��������Ƶ�Эͬ���˵����Ƽ��б�
        if user_cf_buy_rec_dict:
            rec_list.extend([[str(vv) + "_" + k for vv in v] for k, v in user_cf_buy_rec_dict.items()])

        # BPR�����Ƽ�����
        if user_bpr_rec_json is not None:
            user_bpr_rec_dict = json.loads(user_bpr_rec_json).get(cat_id_str, {})

        # ����bpr�Ƽ��б�
        if user_bpr_rec_dict:
            rec_list.extend([[str(vv) + "_" + k for vv in v] for k, v in user_bpr_rec_dict.items()])

        # ��񵵴������Ƽ����Դ���
        if len(json_string_list) != 0:
            pass
            """
            if json_string_list[1] is not None:
                tmp_rec_dict1 = json.loads(json_string_list[1])
                rec_list.append([supply_id + "_" + tmp_rec_dict1['strategy_id'] for supply_id in
                                 tmp_rec_dict1['rec_supplier_list'].split(",")])

            # ��ͳ��ò��Դ���
            if json_string_list[2] is not None:
                tmp_rec_dict2 = json.loads(json_string_list[2])
                rec_list.append([supply_id + "_" + tmp_rec_dict2['strategy_id'] for supply_id in
                                 tmp_rec_dict2['rec_supplier_list'].split(",")[0:5]])
            """
        # �������Ƽ�
        # if user_hoo_profile == 1:
        #     rec_list.append([supply_id + "_" + json.loads(json_string_hoo)['strategy_id'] for supply_id in
        #                      json.loads(json_string_hoo)['rec_supplier_list'].split(",")[0:3]])

        # rec_listΪ�յĻ�ֱ�ӷ��ؿ�
        if len(rec_list) == 0:
            return jsonify({"user_id": user_id,
                            "third_cat_id": cat_id,
                            "scene": scene,
                            "rec_supply_list": []})

        # �����Ƽ�������
        rec_supply_list = []
        for cell in zip_longest(*rec_list):
            rec_supply_list.extend([{"strategy_id": i.split("_")[1], "supply_id": int(i.split("_")[0]),
                                     "market_name": model_pool.get("supply_recommend_data_load").supply_market_dict[
                                         int(i.split("_")[0])],
                                     "rec_reason": str(
                                         eval(rec_recson_random_dict.get(i.split("_")[1], {}).get(scene, "0"))).replace(
                                         '0', "") +
                                                   rec_recson_dict.get(i.split("_")[1], {}).get(scene)} for i in cell if
                                    i is not None])

        # �û��ع��б���
        # ר�����û�����ĵ����б���
        special_date = (datetime.now() - timedelta(hours=7)).strftime('%Y-%m-%d')
        special_date = special_date + ' 07:00:00'
        struct_time = time.strptime(special_date, '%Y-%m-%d %H:%M:%S')
        special_timestamp = time.mktime(struct_time)
        user_page_special_list = []
        if user_page_string is not None:
            user_page_special_list = [int(s_s_t.split('_')[0]) for s_s_t in user_page_string.split(',')
                                      if
                                      int(s_s_t.split('_')[1]) >= special_timestamp and int(s_s_t.split('_')[2]) >= 5]

        timestamp_now = int(time.time())
        user_exposure_list_low, user_exposure_list_up, user_exposure_list_mid = [], [], []
        if user_exposure_string is not None:
            user_exposure_list_low = [int(sp_ts.split('_')[0]) for sp_ts in user_exposure_string.split(',') if
                                      (timestamp_now - int(sp_ts.split('_')[1])) / (24 * 3600) < 0.25]
            user_exposure_list_up = [int(sp_ts.split('_')[0]) for sp_ts in user_exposure_string.split(',') if
                                     (timestamp_now - int(sp_ts.split('_')[1])) / (24 * 3600) <= 3]
            user_exposure_list_mid = [sp for sp in user_exposure_list_up if sp not in user_exposure_list_low]
        # ����ȥ��
        rec_supply_list_filter = []
        filter_list = []
        for rec_cell in rec_supply_list:
            if rec_cell["supply_id"] not in filter_list and rec_cell["supply_id"] not in user_exposure_list_up and \
                    rec_cell["supply_id"] not in user_page_special_list:
                rec_supply_list_filter.append(rec_cell)
                filter_list.append(rec_cell["supply_id"])

        if len(rec_supply_list_filter) >= 10 or len(user_exposure_list_mid) == 0:
            return jsonify({"user_id": user_id,
                            "third_cat_id": cat_id,
                            "scene": scene,
                            "rec_supply_list": rec_supply_list_filter})
        else:
            rec_diff_num = 10 - len(rec_supply_list_filter)
            add_num = 0
            for exp_supply_id in user_exposure_list_mid:
                for rec_cell in rec_supply_list:
                    if rec_cell["supply_id"] == exp_supply_id and rec_cell["supply_id"] not in filter_list and rec_cell[
                        "supply_id"] not in user_page_special_list:
                        rec_supply_list_filter.append(rec_cell)
                        filter_list.append(rec_cell["supply_id"])
                        add_num += 1
                if add_num >= rec_diff_num:
                    break
            return jsonify({"user_id": user_id,
                            "third_cat_id": cat_id,
                            "scene": scene,
                            "rec_supply_list": rec_supply_list_filter})

        # ����ǰ�����û�������ݣ��Դ�ɢ��ʽ�����û����������
        # rec_supply_list_filter = rec_supply_list_filter[0:16]
        # random.shuffle(rec_supply_list_filter)
        #
        # # �Ƽ��б���������ʱɾ���û��ع��б�
        # if (len(user_exposure_list) != 0 and len(rec_supply_list_filter)<=3):  #or len(user_exposure_list) >= 25
        #     pipe.hdel("supply_recommend_exposure", str(user_id)+'_'+cat_id_str)
        #     pipe.execute()


    except Exception as e:
        exstr = traceback.format_exc()
        app.logger.info(exstr)
        app.logger.error(repr(e))
        app.logger.error(f'user_id:{user_id}')
        app.logger.error(f'cat_id:{cat_id}')
        app.logger.info(f'cat_dict:[{model_pool.get("supply_recommend_data_load").cat_dict.get(cat_id)}]')
        return jsonify({"user_id": user_id,
                        "third_cat_id": cat_id,
                        "scene": scene,
                        "rec_supply_list": []})

@main.route('/rank_model/', methods=['POST'])
def rank_model():
    interface_start_time = datetime.now()
    # ������Ϣ
    max_supply_num = app.config.get('MAX_SUPPLY_NUM')
    group_num = app.config.get('GROUP_NUM')
    ES_TOP_N = app.config.get('ES_TOP_N')
    ES_SIZE = app.config.get('ES_SIZE')
    NEW_GOODS_NO_NUM = app.config.get('NEW_GOODS_NO_NUM')
    KEYWORD_GOODS_EMB_DIM = app.config.get('KEYWORD_GOODS_EMB_DIM')
    KEYWORD_SUPPLY_EMB_DIM = app.config.get('KEYWORD_SUPPLY_EMB_DIM')
    SUPPLY_KEYWORD_EMB_DIM = app.config.get('SUPPLY_KEYWORD_EMB_DIM')
    GOODS_KEYWORD_EMB_DIM = app.config.get('GOODS_KEYWORD_EMB_DIM')
    req_data = json.loads(request.data)  # ��json�ַ���תΪdict
    user_id = req_data['user_id']
    keyword = req_data['keyword']
    dsl_json_str = req_data['dsl']
    dsl = json.loads(dsl_json_str)
    app.logger.info(f'user_id��{user_id}')
    app.logger.info(f'keyword��{keyword}')
    size = int(req_data['size'])
    # ���Ĳ��ǵ�һҳ���ڶ�ҳ����������dsl��sql�������offset
    offset = int(req_data['offset'])
    disperse = req_data['disperse']
    app.logger.info(f'disperse��{disperse}')
    device_id = req_data['device_id']
    shunt_id = req_data['shunt_id']
    top_cat = int(req_data['top_cat'])
    dsl['size'] = ES_TOP_N if ES_TOP_N > size else size
    # app.logger.info(f'����json��ӡ��{req_data}')

    pipe = redis.Redis(connection_pool=redis_pool).pipeline()
    redis_key = str(user_id) +'_' + device_id
    resp = {}
    # 1����ȡ��������
    rd_tb = 'search_rank_model'
    if offset == 0:
        #1�������ö��߼����ж�
        dsl_sort_list = dsl.get('sort',[])
        supply_index = -1
        if len(dsl_sort_list) > 0:
            cnt = 0
            for dsl_s in dsl_sort_list:
                if cnt > 3:
                    break
                if '_script' not in dsl_s:
                    cnt += 1
                    continue
                else:
                    if dsl_s.get('_script',{}).get('script',{}).get('params',{}).get('top_supply_id','-1')!='-1':
                        supply_index = cnt
                        break
                    else:
                        cnt += 1
        # 2����ȡ��Ʒ��Ϣ���÷�
        s1 = datetime.now()
        result = fetch_es_data(redis_key, dsl)
        if result['goods_no_list'] is not None and len(result['goods_no_list']) <= 0:
            resp['total'] = 0
            resp['goods_recommend'] = []
            app.logger.info(f'�ӿ�ִ��ʱ�䣺{datetime.now() - interface_start_time}��user_id��{user_id}��keyword��{keyword}')
            return resp
        app.logger.info(f'����es��ʱ�䣺{datetime.now() - s1}')
        # 3����ȡ�û�β��,��ʱ����
        # user_tail = lastNumbyShuntID(shunt_id=shunt_id, user_id=user_id)
        # ���Ŵ���
        goods_no_list = [obj['goods_no'] for obj in result['goods_no_list']]
        # app.logger.info(goods_no_list[0:5])
        goods_no_len = len(goods_no_list)
        goods_no_str = ','.join(goods_no_list)
        goods_no_tuple = eval(goods_no_str)
        # supply����
        supply_id_list = [obj['supply_id'] for obj in result['goods_no_list']]
        supply_id_tuple = eval(','.join(supply_id_list))

        # replace = goods_sql.replace('<goods_nos/>', goods_no_str)
        # m1 = datetime.now()
        # goods_no_portrait = mysql_pool.getAll(replace)
        # app.logger.info(f'goods_no_portrait_time��{datetime.now() - m1}')
        # redis��ȡ�û�/��Ʒ����

        r1 = datetime.now()
        pipe.hmget('goods_feature1', goods_no_tuple)
        pipe.hget('user_offline_feature1', user_id)
        pipe.hget('user_real_time_feature1', user_id)
        pipe.hget('keyword_supply_name_emb', keyword)
        pipe.hget('keyword_goods_name_emb', keyword)
        pipe.hmget('goods_name_keyword_emb', goods_no_tuple)
        pipe.hmget('supply_name_keyword_emb', supply_id_tuple)
        pipe.hget('user_buy_suppress', user_id)
        results = pipe.execute()
        app.logger.info(f'redis_get_data_time��{datetime.now() - r1}')


        goods_feature, redis_user_offline_feature, redis_user_real_time_feature,keyword_supply_embedding, keyword_goods_embedding, goods_no_embedding_redis, supply_id_embedding_redis, user_buy_str = results
        if str(user_id) == '9916952':
            app.logger.info(redis_user_offline_feature)
            app.logger.info(redis_user_real_time_feature)
            app.logger.info(user_buy_str)
        m1 = datetime.now()

        goods_es_data_ = []
        goods_es_data_not_ = []
        goods_no_portrait_use_filter = []
        goods_no_embedding = []
        supply_id_embedding = []
        goods_no_portrait_notuse_filter = []
        goods_feature_len = len(goods_feature)

        app.logger.info(f'goods_feature_loss��{goods_no_len - goods_feature_len}')

        goods_market_area_dict = {}
        for idx in range(goods_feature_len):
            if goods_feature[idx] is not None:
                goods_nos = json.loads(goods_feature[idx])
                goods_nos.update({'goods_no':int(goods_no_list[idx])})
                if goods_nos['low_perform_for_supply'] == 1 or goods_nos['high_sale_high_perform'] == 1 or goods_nos['supply_gmv_copy'] == 1 or goods_nos['supply_sham_sales_cat'] == 1 or goods_nos['is_stockout'] == 1:
                    goods_no_portrait_notuse_filter.append(goods_no_list[idx])
                else:
                    goods_market_area_dict.update({goods_no_list[idx]:{"area":goods_nos.get("area",{}),
                                                                       'big_market_id':goods_nos.get("big_market_id",-999),
                                                                       'result_market_id':goods_nos.get("result_market_id",-999),
                                                                       "tag":goods_nos.get("tag",[]),
                                                                       "primary_cat_id":goods_nos.get("primary_cat_id",-999),
                                                                       "second_cat_id":goods_nos.get("second_cat_id",-999)
                                                                       }})
                    goods_nos.pop('area')
                    goods_nos.pop('tag')
                    goods_no_portrait_use_filter.append(goods_nos)
                    goods_no_embedding.append(goods_no_embedding_redis[idx])
                    supply_id_embedding.append(supply_id_embedding_redis[idx])

            else:
                continue

        # �ѹ���ѹ����
        if user_buy_str is not None:
            sup_t = datetime.now()
            # �û��ѹ���Ʒ�б�
            user_buy_list = [int(buy_no) for buy_no in user_buy_str.split(',')]
            buy_idx_list = [buy_idx for buy_idx in range(len(goods_no_portrait_use_filter)) if goods_no_portrait_use_filter[buy_idx]['goods_no'] in user_buy_list]
            goods_no_portrait_use_filter_buy_list = [goods_no_portrait_use_filter[goods_filter_no_idx]['goods_no'] for goods_filter_no_idx in  buy_idx_list]

            goods_no_portrait_use_filter = [goods_no_portrait_use_filter[goods_por_idx] for goods_por_idx in range(len(goods_no_portrait_use_filter)) if goods_por_idx not in  buy_idx_list]
            goods_no_embedding = [goods_no_embedding[goods_emb_idx] for goods_emb_idx in range(len(goods_no_embedding)) if goods_emb_idx not in  buy_idx_list]
            supply_id_embedding = [supply_id_embedding[supply_emb_idx] for supply_emb_idx in range(len(supply_id_embedding)) if supply_emb_idx not in  buy_idx_list]


            goods_no_portrait_notuse_filter =  [str(user_buy_no) for user_buy_no in goods_no_portrait_use_filter_buy_list if str(user_buy_no) not in goods_no_portrait_notuse_filter] + goods_no_portrait_notuse_filter
            app.logger.info(f'goods_no_sup��{datetime.now() - sup_t}')

        for es in result['goods_no_list']:
            if es['goods_no'] in goods_no_portrait_notuse_filter:
                goods_es_data_not_.append(es)
            else:
                goods_es_data_.append(es)

        app.logger.info(f'goods_no_portrait_process��{datetime.now() - m1}')

        if len(goods_es_data_)<=0 or len(goods_no_portrait_use_filter)<=0:
            goods_es_data = result['goods_no_list']
        else:
            down_goods_num = len(goods_no_portrait_notuse_filter)
            app.logger.info(f'down_goods_num��{down_goods_num}')
            # 4������ģ��
            model1 = datetime.now()
            # redis��ȡ�ִ�����
            """
            jbs = datetime.now()
            token_list = jieba.lcut(keyword)
            app.logger.info(f'jieba_time��{datetime.now() - jbs}')
            r1 = datetime.now()
            for token in token_list:
                app.logger.info(token)
                pipe.hget('keyword_embedding', token)
                pipe.hget('idf', token)
            """
            rp = datetime.now()
            # keyword emb����
            keyword_embedding_list = []
            # keyword_supply_emb
            if keyword_supply_embedding is not None:
                keyword_supply_dict = json.loads(keyword_supply_embedding)
                keyword_embedding_list.extend(keyword_supply_dict.get('keyword_supply_name_emb',[0.0]*KEYWORD_SUPPLY_EMB_DIM))
            else:
                keyword_embedding_list.extend([0.0]*KEYWORD_SUPPLY_EMB_DIM)

            # keyword_goods_emb
            if keyword_goods_embedding is not None:
                keyword_goods_dict = json.loads(keyword_goods_embedding)
                keyword_embedding_list.extend(keyword_goods_dict.get('keyword_goods_name_emb',[0.0]*KEYWORD_GOODS_EMB_DIM))
            else:
                keyword_embedding_list.extend([0.0]*KEYWORD_GOODS_EMB_DIM)

            # goods_no emb����
            supply_goods_embedding_list = []
            for g_i in range(len(goods_no_embedding)):
                if goods_no_embedding[g_i] is not None:
                    tmp_goods_dict = json.loads(goods_no_embedding[g_i])
                    tmp_supply_goods_name_emb =[goods_no_portrait_use_filter[g_i]['goods_no']] + tmp_goods_dict.get('goods_name_keyword_emb',[0.0]*GOODS_KEYWORD_EMB_DIM)
                else:
                    tmp_supply_goods_name_emb =[goods_no_portrait_use_filter[g_i]['goods_no']] + [0.0] * GOODS_KEYWORD_EMB_DIM

                if supply_id_embedding[g_i] is not None:
                    tmp_supply_dict = json.loads(supply_id_embedding[g_i])
                    tmp_supply_goods_name_emb.extend(tmp_supply_dict.get('supply_name_keyword_emb',[0.0]*SUPPLY_KEYWORD_EMB_DIM))
                else:
                    tmp_supply_goods_name_emb.extend([0.0] * SUPPLY_KEYWORD_EMB_DIM)

                supply_goods_embedding_list.append(tmp_supply_goods_name_emb)

            app.logger.info(f'process_embedding_data_time��{datetime.now() - rp}')
            app.logger.info(f'topcat��{top_cat}')
            app.logger.info(f'supply_index��{supply_index}')

            if len(goods_es_data_) > ES_SIZE:
                goods_es_data_rank = goods_es_data_[0:ES_SIZE]
                goods_es_data_rank_not = goods_es_data_[ES_SIZE:]
            else:
                goods_es_data_rank = goods_es_data_
                goods_es_data_rank_not = []

            goods_es_data = model_pool.get("ctrcvrlgb") \
                .predict(user_id, redis_user_offline_feature, redis_user_real_time_feature , goods_es_data_rank, goods_no_portrait_use_filter,
                         top_cat,
                         app.config.get('USER_PROFILE_COLUMNS'), supply_index, keyword_embedding_list, supply_goods_embedding_list,KEYWORD_SUPPLY_EMB_DIM,KEYWORD_GOODS_EMB_DIM,GOODS_KEYWORD_EMB_DIM,SUPPLY_KEYWORD_EMB_DIM, goods_market_area_dict, 0)

            if str(user_id) == '9916952':
                app.logger.info(goods_es_data[:5])

            goods_es_data = goods_es_data + goods_es_data_rank_not+goods_es_data_not_

            app.logger.info(f'model_time��{datetime.now() - model1}')

        new_goods_data = [goods for goods in goods_es_data if goods.get('sort_factor_is_new', 0) == 1][0:NEW_GOODS_NO_NUM]

        app.logger.info(f'new_len��{len(new_goods_data)}')
    else:
        pipe.hget(rd_tb, redis_key)
        redis_result = pipe.execute()[0]
        if redis_result is not None:
            result = json.loads(redis_result)
            resp['total'] = result['first_total']
            first_total = ES_TOP_N if result['first_total'] >= ES_TOP_N else result['first_total']
            # if (offset + 1) * size > first_total:
            if offset + size <= first_total:
                goods_es_data = result['goods_no_list']
                new_goods_data = result['new_goods_data']
            elif offset < first_total:
                # if first_total < offset + size:
                # ��(offset - 1) * size < total ��offset * size > totalʱ����ȡ�����ϵ�������ȡes�������
                dsl['size'] = offset + size - first_total
                dsl['from'] = first_total
                app.logger.info(f'dsl-size:'+str(dsl['size']))
                app.logger.info(f'dsl-from:'+str(dsl['from']))
                temp_goods_no_list = result['goods_no_list']
                result['goods_no_list'] = []
                result['new_goods_data'] = []
                result['total'] = 0
                result['size'] = size
                result['offset'] = offset
                result['dt'] = datetime.now().strftime('%Y%m%d')
                pipe.hset(rd_tb, redis_key, json.dumps(result))
                pipe.execute()

                if first_total < ES_TOP_N:
                    resp['goods_recommend'] = result['goods_no_list']
                    app.logger.info(f'�ӿ�ִ��ʱ�䣺{datetime.now() - interface_start_time}��user_id��{user_id}��keyword��{keyword}')
                    return resp
                else:
                    es_result = fetch_es_data(user_id, dsl)
                    app.logger.info(f"goods_no_list_redis: {len(['goods_no_list'])} ��es_goods_no_list : [{len(es_result['goods_no_list'])}]")
                    resp['goods_recommend'] = temp_goods_no_list + es_result['goods_no_list']
                    app.logger.info(f'�ӿ�ִ��ʱ�䣺{datetime.now() - interface_start_time}��user_id��{user_id}��keyword��{keyword}')
                    return resp
            else:
                if first_total < ES_TOP_N:
                    resp['goods_recommend'] = []
                    app.logger.info(f'�ӿ�ִ��ʱ�䣺{datetime.now() - interface_start_time}��user_id��{user_id}��keyword��{keyword}')
                    return resp
                dsl['size'] = size
                dsl['from'] = offset
                es_result = fetch_es_data(user_id, dsl)
                resp['goods_recommend'] = es_result['goods_no_list']
                app.logger.info(f'�ӿ�ִ��ʱ�䣺{datetime.now() - interface_start_time}��user_id��{user_id}��keyword��{keyword}')
                return resp
        else:
            resp['goods_recommend'] = []
            resp['total'] = 0
            app.logger.info(f'�ӿ�ִ��ʱ�䣺{datetime.now() - interface_start_time}��user_id��{user_id}��keyword��{keyword}')
            return resp

    goods_recommend = []  # �ӿڷ��ظ���˵��Ƽ��б�
    goods_es_data_ = goods_es_data
    new_goods_data_ = new_goods_data
    start_time = datetime.now()
    user_rec_len = len(goods_es_data)
    del_list = []
    sort1 = datetime.now()
    if disperse =='1':
        # ��ɢ
        # goods_recommend_str = []
        while len(goods_recommend) < size and len(goods_recommend) + len(del_list) != user_rec_len:
            del_list = []
            if_new_list = []
            cnt = 0
            supply_list = []
            for goods in goods_es_data:

                if_new = goods.get('sort_factor_is_new',0)
                supply = goods.get('supply_id','')

                supply_list.append(supply)  # supply array ���ڼ����x����Ʒ���ڳ��ֵĴ���
                if_new_list.append(if_new)

                # ��ɢ�����������Ʒ���������ִ����Ѿ�����max_supply_num���򽫸���Ʒ����del_list�б�
                if (supply and np.sum(np.asarray(supply_list) == supply) > max_supply_num) or np.sum(if_new_list) > max_supply_num:
                    del_list.append(goods)
                    if_new_list.pop()
                    supply_list.pop()
                    continue

                goods_recommend.append(goods)
                # goods_recommend_str.append(goods['goods_no'])
                if if_new and len(new_goods_data)>0:
                    new_goods_data.pop(0)
                if len(goods_recommend) == size:
                    break
                cnt += 1
                if cnt == group_num:
                    if np.sum(if_new_list) == 0 and len(new_goods_data) > 0:
                        if goods_recommend[-1]['score'] <= new_goods_data[0]['score']:
                            goods_recommend.insert(-1, new_goods_data.pop(0))
                            del_list.append(goods_recommend.pop())
                    break
            # ����goods_es_data����δ���Ч��Ӧ�ñȽϵ�
            goods_es_data = [tmp_goods for tmp_goods in goods_es_data if tmp_goods not in goods_recommend]
        app.logger.info(f'����ʱ�䣺{datetime.now() - sort1}')
        # �����Ʒ�б�û�ж�����Ʒ����del_listƴ�ӵ�֮ǰ�б�
        if len(goods_recommend) < size and len(del_list) != 0:
            del_add_rec = del_list[:size - len(goods_recommend)]
            goods_recommend = goods_recommend + del_add_rec
            app.logger.info('ɾ��')
            #app.logger.info(f'���˲��ֲ�Ϊ��������û����棬��һ�ε��� {len([d_l for d_l in del_list if d_l not in del_add_rec])}')  # ���˲��ֲ�Ϊ��������û����棬��һ�ε���
        else:
            app.logger.info(f'goods_es_data_len��{len(goods_es_data)}')  # ���˲��ֲ�Ϊ��������û����棬��һ�ε���

    else:
        #     ������Ҫ��ɢ��ʱ��
        while len(goods_recommend) < size and len(goods_recommend) + len(del_list) != user_rec_len:
            del_list = []
            if_new_list = []
            cnt = 0
            for goods in goods_es_data:

                if_new = goods.get('sort_factor_is_new',0)
                if_new_list.append(if_new)

                # ��ɢ�����������Ʒ���������ִ����Ѿ�����max_supply_num���򽫸���Ʒ����del_list�б�
                if np.sum(if_new_list) > max_supply_num:
                    del_list.append(goods)
                    if_new_list.pop()
                    continue

                goods_recommend.append(goods)

                if if_new and len(new_goods_data)>0:
                    new_goods_data.pop(0)

                if len(goods_recommend) == size:
                    break

                cnt += 1
                if cnt == group_num:
                    if np.sum(if_new_list) == 0 and len(new_goods_data) > 0:
                        if goods_recommend[-1]['score'] <= new_goods_data[0]['score']:
                            goods_recommend.insert(-1, new_goods_data.pop(0))
                            del_list.append(goods_recommend.pop())
                    break
            # app.logger.info(if_new_list)
            # ����goods_es_data����δ���Ч��Ӧ�ñȽϵ�
            goods_es_data = [tmp_goods for tmp_goods in goods_es_data if tmp_goods not in goods_recommend]
        if len(goods_recommend) < size and len(del_list) != 0:
            del_add_rec = del_list[:size - len(goods_recommend)]
            goods_recommend = goods_recommend + del_add_rec
            app.logger.info('ɾ��')
            #app.logger.info(f'���˲��ֲ�Ϊ��������û����棬��һ�ε��� {len([d_l for d_l in del_list if d_l not in del_add_rec])}')  # ���˲��ֲ�Ϊ��������û����棬��һ�ε���
        else:
            app.logger.info(len(goods_es_data))  # ���˲��ֲ�Ϊ��������û����棬��һ�ε���
    app.logger.info('�����ʱ��{}'.format(datetime.now() - start_time))
    # 7��ȥ�����ظ��û������ݣ������»�������
    result['goods_no_list'] = [tmp_goods for tmp_goods in goods_es_data_ if tmp_goods not in goods_recommend]
    result['new_goods_data'] = [tmp_goods for tmp_goods in new_goods_data_ if tmp_goods not in goods_recommend]
    result['total'] = len(result['goods_no_list'])
    result['size'] = size
    result['offset'] = offset
    result['disperse'] = disperse
    result['dt'] = datetime.now().strftime('%Y%m%d')
    resp['goods_recommend'] = goods_recommend
    resp['total'] = result['first_total']
    r2 = datetime.now()
    pipe.hset(rd_tb, redis_key, json.dumps(result))
    pipe.execute()
    app.logger.info(f'reids����ʱ�䣺{datetime.now() - r2}')
    app.logger.info(f'�ӿ�ִ��ʱ�䣺{datetime.now() - interface_start_time}��user_id��{user_id}��keyword��{keyword}')
    return resp

# ģ�ͼ��ؽӿ�
@main.route('/load/model', methods=['POST'])
def load_model_file():
    downloadPaths = []
    # ���մ���json��������
    data = json.loads(request.data)  # ��json�ַ���תΪdict
    file_names = data['file_names']
    model_name = data['model_name']
    for file_name in file_names.split(','):
        # ��ȡOBS����
        load_models(file_name)
        index = file_name.rindex('/')
        downloadPaths.append('./model_files/' + file_name[(index + 1):])
    try:
        # services.init.similar = Similar4OldGood(downloadPaths[0], downloadPaths[1], downloadPaths[2], downloadPaths[3])
        # services.init.similar.load_model(paths=downloadPaths)
        model_pool.get(model_name).load_model(paths=downloadPaths)
        return jsonify({"code": 200, "msg": "���سɹ�"})
    except Exception as e:
        app.logger.error(repr(e))
        return jsonify({"code": 500, "msg": "��������ʧ��"})