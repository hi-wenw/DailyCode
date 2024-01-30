from concurrent.futures import ThreadPoolExecutor
import threading
import queue


def dance(num):
    with lock:
        current_num = num
        print(f'I am dancing==========={current_num}===========,{threading.currentThread()}')


if __name__ == '__main__':
    lock = threading.Lock()
    queue_list = queue.Queue()
    for i in range(100):
        queue_list.put(i)

    pool = ThreadPoolExecutor(max_workers=100)

    for i in range(queue_list.qsize()):
        pool.submit(dance, queue_list.get())

