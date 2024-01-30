# from concurrent.futures import ThreadPoolExecutor
# import threading
# import time
# import random
#
#
# def task(i):
#     sleep_seconds = random.randint(1, 3)  # 随机睡眠时间
#     print('线程名称：%s，参数：%s，睡眠时间：%s' % (threading.current_thread().name, i, sleep_seconds))
#     time.sleep(sleep_seconds)  # 定义睡眠时间
#
#
# if __name__ == '__main__':
#     pool = ThreadPoolExecutor(max_workers=2)  # 定义线程
#
#     for i in range(10):
#         future1 = pool.submit(task, i)
#         future1.result()


