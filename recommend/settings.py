from logging.config import dictConfig

dictConfig({
    "env": {
        "FLASK_APP": "recommend_app"
    },
    "version": 1,
    "disable_existing_loggers": False,  # 不覆盖默认配置
    "formatters": {  # 日志输出样式
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",  # 控制台输出
            "level": "INFO",
            "formatter": "default",
        },
        "log_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "default",  # 日志输出样式对应formatters
            "filename": "./logs/recommendation_api_servers.log",  # 指定log文件目录
            "maxBytes": 50 * 1024 * 1024,  # 文件最大50M
            "backupCount": 10,  # 最多10个文件
            "encoding": "utf8",  # 文件编码
        },

    },
    "root": {
        "level": "DEBUG",  # # handler中的level会覆盖掉这里的level
        "handlers": ["console", "log_file"]
    }
})

class BaseConfig():
    """通用基础配置"""

class TestConfig(BaseConfig):
    """测试环境配置"""
    REDIS_HOST = '139.159.134.78'
    REDIS_DB = 0
    REDIS_PORT = 16379
    REDIS_PASSWORD = 'm6ojIOg1rvcc5go8'

    # 模型配置
    ID_GOODS_PATH = "D:/Data/data/embedding/id_to_goods.pkl"
    GOODS_ID_PATH = "D:/Data/data/embedding/goods_to_id.pkl"
    MODEL_GOODS_EMBEDDING_PATH = "D:/Data/data/embedding/emgoods_index_embedding.pk"
    MODEL_GOODS_EMBEDDING_FAISS_INDEX_PATH = "D:/Data/data/embedding/emgoods_index.index"

class ZYConfig(BaseConfig):
    """测试环境配置"""
    REDIS_HOST = '139.159.134.78'
    REDIS_DB = 0
    REDIS_PORT = 16379
    REDIS_PASSWORD = 'm6ojIOg1rvcc5go8'
    REDIS_MAX_CONNECTIONS = 1000

    # 模型配置
    ID_GOODS_PATH = "recommend_online_cache/bpr_embedding/id_to_goods.pkl"
    GOODS_ID_PATH = "recommend_online_cache/bpr_embedding/goods_to_id.pkl"
    MODEL_GOODS_EMBEDDING_PATH = "recommend_online_cache/bpr_embedding/emgoods_index_embedding.pk"
    MODEL_GOODS_EMBEDDING_FAISS_INDEX_PATH = "recommend_online_cache/bpr_embedding/emgoods_index.index"
    TOP_K = 200

    # 档口推荐文件配置
    # 类别id-类别名字典
    SUPPLY_RECOMMEND_CAT_DICT_PATH = "recommend_online_cache/supply_recommend/cat_dict.pkl"
    # 档口id-大市场名
    SUPPLY_RECOMMEND_SUPPLY_MARKET_DICT_PATH = "recommend_online_cache/supply_recommend/supply_market_dict.pkl"

    OBS_AK = 'EULIXLKJQLUS62GPNIAX'
    OBS_SK = 'vmoTDJVUOXVtwt8pwh5LQ6LnE2bJPDtxid7biimK'
    OBS_SERVER = 'obs.cn-south-1.myhuaweicloud.com'
    BUCKET_NAME = "yishou_flask-data"
    # MYSQL_HOST = '121.37.27.174'
    MYSQL_HOST = '121.37.244.90'
    MYSQL_PORT = '3306'
    # MYSQL_USER = 'fmdes_user'
    MYSQL_USER = 'root'
    # MYSQL_PASSWORD = '6IveUZJyx1ifeWGq'
    MYSQL_PASSWORD = 'JjE)WIN&b3=j'
    MYSQL_DB_NAME = 'yishou_algorithm_production'

    ES_HOSTS = ['192.168.1.221']
    SNIFF_ON_START = True
    SNIFF_ON_CONNECTION_FAIL = True
    SNIFF_TIMEOUT = 60
    ES_SIZE = 300
    CTRCVRLGB_CTR_MODEL_PATH ="recommend_online_cache/ctrcvr_model/ctr_model.pkl"
    CTRCVRLGB_CVR_MODEL_PATH ="recommend_online_cache/ctrcvr_model/cvr_model.pkl"
    CTR_COLUMNS_DICT_PATH = "recommend_online_cache/ctrcvr_model/ctr_columns.pickle"
    CVR_COLUMNS_DICT_PATH = "recommend_online_cache/ctrcvr_model/cvr_columns.pkl"

    ES_TOP_N = 300
    KEYWORD_EMB_DIM = 16
    SUPPLY_EMB_DIM = 8
    GOODS_EMB_DIM = 16
    MAX_SUPPLY_NUM = 3      # 连续x个商品里，相同档口最多出现的次数
    GROUP_NUM = 8           # 推荐列表数量每到group_num的倍数后，将排除档口的商品加入列表重新打散
    NEW_GOODS_NO_NUM = 5    # 新款置顶数量
    USER_PROFILE_COLUMNS = [
        "orders",
        "torders",
        "thirty_days_goods",
        "r",
        "is_b_port_v1",
        "value_level",
        "user_net_worth",
        "dwt_user_third_cat_grade_score_30day_score",
        "dwt_user_third_cat_supply_score_30day_score",
        "goods_preference_level",
        "good_category_grade_second_id",
        "good_category_grade_third_id",
        # "user_style_id",
        "user_buyer_id",
        "user_supply_id",
        "market_first_id",
        "market_second_id",
        "pay_orders",
        "u2s_180_score",
        "app_start_count",
        "goods_exposure_count",
        "goods_click_count",
        "real_goods_buy_num",
        "goods_add_cart_count",
        "goods_no_click_count",
        "goods_collect_count",
        "u_all_180_score",
        "search_click_pv",
        "u2g_s_score_180",
        "u2g_180_score",
        "search_exposure_pv",
        "search_add_cart_pv",
        "stall_page_add_cart_pv",
        "search_real_buy_user_num",
        "u2grade_score_180",
        # "u2grade_s_score_180",
        "u2style_score_180",
        "u2_3cat_grade_score_180",
        "u2_3cat_score_180",
        "u2_3cat_supply_score_180",
        "u2_3cat_style_score_180",
        "exposure_cnt_3",
        "click_cnt_3",
        "3uclick_mean",
        "3uclick_cnt_2",
        "exposure_click_ratio_3",
        "exposure_click_std_3",
        "add_cart_cnt_3",
        "click_add_cart_ratio_3",
        "click_add_cart_std_3",
        # "add_cart_mean_3",
        "app_start_count_sum_3",
        # "goods_exposure_count_sum_3",
        # "goods_click_count_sum_3",
        "real_goods_buy_num_sum_3",
        # "goods_add_cart_count_sum_3",
        # "goods_non_click_count_sum_3",
        "goods_collect_count_sum_3",
        "pay_order_count_sum_3",
        # "app_start_count_mean_3",
        "goods_exposure_count_mean_3",
        "goods_click_count_mean_3",
        # "real_goods_buy_num_mean_3",
        "goods_add_cart_count_mean_3",
        # "goods_non_click_count_mean_3",
        "goods_collect_count_mean_3",
        # "pay_order_count_mean_3",
        "app_start_count_std_3",
        "goods_exposure_count_std_3",
        "goods_click_count_std_3",
        "real_goods_buy_num_std_3",
        "goods_add_cart_count_std_3",
        # "goods_non_click_count_std_3",
        "goods_collect_count_std_3",
        "pay_order_count_std_3",
        'dwt_user_third_cat_bpr_score_15day_score',
        'dwt_user_third_cat_supply_bpr_score_15day_score',
        'dwt_user_third_cat_grade_bpr_score_15day_score',
        'dwt_user_third_cat_style_bpr_score_15day_score',
        "dwt_user_third_cat_grade_score_strategy_v1_15day_score",
        "dwt_user_third_cat_grade_score_strategy_v1_30day_score",
        "dwt_user_third_cat_grade_score_strategy_v1_180day_score"
    ]

class PRODConfig(BaseConfig):
    """生产环境配置"""
    REDIS_HOST = '192.168.4.215'
    REDIS_DB = 0
    REDIS_PORT = 6379
    REDIS_PASSWORD = 'm6ojIOg1rvcc5go8'

    # 模型配置
    ID_GOODS_PATH = "recommend_online_cache/bpr_embedding/id_to_goods.pkl"
    GOODS_ID_PATH = "recommend_online_cache/bpr_embedding/goods_to_id.pkl"
    MODEL_GOODS_EMBEDDING_PATH = "recommend_online_cache/bpr_embedding/emgoods_index_embedding.pk"
    MODEL_GOODS_EMBEDDING_FAISS_INDEX_PATH = "recommend_online_cache/bpr_embedding/emgoods_index.index"
    SUPPLY_RECOMMEND_INDEX_PATH = "recommend_online_cache/bpr_embedding/emgoods_index.index"
    TOP_K = 200

    # 档口推荐文件配置
    # 类别id-类别名字典
    SUPPLY_RECOMMEND_CAT_DICT_PATH = "recommend_online_cache/supply_recommend/cat_dict.pkl"
    # 档口id-大市场名
    SUPPLY_RECOMMEND_SUPPLY_MARKET_DICT_PATH = "recommend_online_cache/supply_recommend/supply_market_dict.pkl"

    OBS_AK = 'EULIXLKJQLUS62GPNIAX'
    OBS_SK = 'vmoTDJVUOXVtwt8pwh5LQ6LnE2bJPDtxid7biimK'
    OBS_SERVER = 'obs.cn-south-1.myhuaweicloud.com'
    BUCKET_NAME = "yishou_flask-data"
    MYSQL_HOST = '192.168.6.115'
    MYSQL_PORT = '3306'
    MYSQL_USER = 'data_user'
    MYSQL_PASSWORD = 'tyzUu9Da4xvNXdY4'
    MYSQL_DB_NAME = 'yishou_algorithm_production'

    ES_HOSTS = ['192.168.8.60', '192.168.8.246', '192.168.8.229', '192.168.8.55', '192.168.8.119', '192.168.8.136',
                '192.168.8.4', '192.168.8.85', '192.168.8.17']
    SNIFF_ON_START = True
    SNIFF_ON_CONNECTION_FAIL = True
    SNIFF_TIMEOUT = 60
    ES_SIZE = 360
    CTRCVRLGB_CTR_MODEL_PATH ="recommend_online_cache/ctrcvr_model/ctr_model.pkl"
    CTRCVRLGB_CVR_MODEL_PATH ="recommend_online_cache/ctrcvr_model/cvr_model.pkl"
    CTR_COLUMNS_DICT_PATH = "recommend_online_cache/ctrcvr_model/ctr_columns.pickle"
    CVR_COLUMNS_DICT_PATH = "recommend_online_cache/ctrcvr_model/cvr_columns.pkl"

    ES_TOP_N = 520

    KEYWORD_GOODS_EMB_DIM = 16
    KEYWORD_SUPPLY_EMB_DIM = 16
    SUPPLY_KEYWORD_EMB_DIM = 16
    GOODS_KEYWORD_EMB_DIM = 16

    MAX_SUPPLY_NUM = 3      # 连续x个商品里，相同档口最多出现的次数
    GROUP_NUM = 8           # 推荐列表数量每到group_num的倍数后，将排除档口的商品加入列表重新打散
    NEW_GOODS_NO_NUM = 20   # 新款置顶数量
    USER_PROFILE_COLUMNS = [
        "orders",
        "torders",
        "thirty_days_goods",
        "r",
        "is_b_port_v1",
        "value_level",
        "user_net_worth",
        "dwt_user_third_cat_grade_score_30day_score",
        "dwt_user_third_cat_supply_score_30day_score",
        "goods_preference_level",
        "good_category_grade_second_id",
        "good_category_grade_third_id",
        # "user_style_id",
        "user_buyer_id",
        "user_supply_id",
        "market_first_id",
        "market_second_id",
        "pay_orders",
        "u2s_180_score",
        "app_start_count",
        "goods_exposure_count",
        "goods_click_count",
        "real_goods_buy_num",
        "goods_add_cart_count",
        "goods_no_click_count",
        "goods_collect_count",
        "u_all_180_score",
        "search_click_pv",
        "u2g_s_score_180",
        "u2g_180_score",
        "search_exposure_pv",
        "search_add_cart_pv",
        "stall_page_add_cart_pv",
        "search_real_buy_user_num",
        "u2grade_score_180",
        # "u2grade_s_score_180",
        "u2style_score_180",
        "u2_3cat_grade_score_180",
        "u2_3cat_score_180",
        "u2_3cat_supply_score_180",
        "u2_3cat_style_score_180",
        "exposure_cnt_3",
        "click_cnt_3",
        "3uclick_mean",
        "3uclick_cnt_2",
        "exposure_click_ratio_3",
        "exposure_click_std_3",
        "add_cart_cnt_3",
        "click_add_cart_ratio_3",
        "click_add_cart_std_3",
        # "add_cart_mean_3",
        "app_start_count_sum_3",
        # "goods_exposure_count_sum_3",
        # "goods_click_count_sum_3",
        "real_goods_buy_num_sum_3",
        # "goods_add_cart_count_sum_3",
        # "goods_non_click_count_sum_3",
        "goods_collect_count_sum_3",
        "pay_order_count_sum_3",
        # "app_start_count_mean_3",
        "goods_exposure_count_mean_3",
        "goods_click_count_mean_3",
        # "real_goods_buy_num_mean_3",
        "goods_add_cart_count_mean_3",
        # "goods_non_click_count_mean_3",
        "goods_collect_count_mean_3",
        # "pay_order_count_mean_3",
        "app_start_count_std_3",
        "goods_exposure_count_std_3",
        "goods_click_count_std_3",
        "real_goods_buy_num_std_3",
        "goods_add_cart_count_std_3",
        # "goods_non_click_count_std_3",
        "goods_collect_count_std_3",
        "pay_order_count_std_3",
        'dwt_user_third_cat_bpr_score_15day_score',
        'dwt_user_third_cat_supply_bpr_score_15day_score',
        'dwt_user_third_cat_grade_bpr_score_15day_score',
        'dwt_user_third_cat_style_bpr_score_15day_score',
        # V2版本新增
        # 用户统计特征
        "user_last_hour_click_cnt",
        "user_today_click_total_cnt",
        "user_click_hour_chain",
        "user_last_hour_add_cart_cnt",
        "user_today_add_cart_total_cnt",
        "user_add_cart_hour_chain",
        # 数据上层有cat
        "cat_last_hour_click_cnt",
        "cat_today_click_total_cnt",
        "cat_click_hour_chain",
        "cat_last_hour_add_cart_cnt",
        "cat_today_add_cart_total_cnt",
        "cat_add_cart_hour_chain",
        # 用户偏好
        "ads_user_preference_score",# 普通180 d
        "ads_user_preference_score_sp_dt_market_score",# 普通30 d
        "third_cat_big_market_bpr_score_15day",# bpr15 d
        "dwt_user_third_cat_grade_score_strategy_v1_15day_score",# 普通15 d
        "dwt_user_third_cat_grade_score_strategy_v1_30day_score",# 普通30 d
        "dwt_user_third_cat_grade_score_strategy_v1_180day_score",# 普通180 d
        # 用户区域商品交互
        "exposure_uv",
        "click_uv",
        "ctr",
        "ctr_wilson_score",
        "add_cart_pv",
        "add_cart_uv",
        "click_pv",
        "cvr",
        "cvr_wilson_score",
        "exposure_pv",
        "order_pv",
        "order_uv",
        # V3版本新增
        # bpr15
        "dwt_user_third_cat_tag_bpr_score_15day_score_avg",
        "dwt_user_third_cat_tag_bpr_score_15day_score_sum",
        #180
        'primary_cat_score',
        'second_cat_score',
        'primary_cat_supply_score',
        'second_cat_supply_score',
        'second_market_score',
        'primary_market_score',
        'big_market_score',
        # basic
        'pay_order_count_sum_7',
        'pay_order_count_mean_7',
        'pay_order_count_std_7',
        # 价格区间特征
        "user_add_cart_max_shop_price",
        "user_add_cart_min_shop_price",
        "user_add_cart_std_shop_price",
        "user_add_cart_mean_shop_price"
    ]

class DevConfig(BaseConfig):
    """开发环境配置"""
    REDIS_HOST = '192.168.4.215'
    REDIS_DB = 0
    REDIS_PORT = 6379
    REDIS_PASSWORD = 'm6ojIOg1rvcc5go8'

