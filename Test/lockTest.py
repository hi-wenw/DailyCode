import threading
from concurrent.futures import ThreadPoolExecutor
from timeit import Timer



def sub():
    global i
    with lock:
        for i in range(10000000):
            i -= 1


def add():
    global i
    with lock:
        for i in range(10000000):
            i += 1


if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=2)
    lock = threading.Lock
    i = 0
    pool.submit(add)
    pool.submit(sub)
    print(i)


