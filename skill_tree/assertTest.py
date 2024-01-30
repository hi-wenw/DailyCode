import time

class TimeSpan:
    def __init__(self):
        self.start = None

    def __enter__(self):
        self.start = time.time()
        return self.start

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        print('耗时: {} 秒'.format(end - self.start))


if __name__ == '__main__':
    with TimeSpan() as t:
        for i in range(0, 1000):
            print(i)