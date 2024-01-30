from concurrent.futures import ThreadPoolExecutor
import threading

# 全局变量，用于记录已经打印的数字
printed_numbers = set()


def print_number(number):
    # 判断该数字是否已经被打印过
    if number in printed_numbers:
        return

    # 使用锁来确保多线程环境下打印的互斥性
    with lock:
        print(number)
        printed_numbers.add(number)


if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=5)  # 定义线程池
    lock = threading.Lock()  # 定义锁对象

    # 提交任务给线程池，每个任务打印一个数字
    for number in range(101):
        pool.submit(print_number, number)