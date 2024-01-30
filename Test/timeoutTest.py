import requests


def reques():
    while True:
        try:
            r = requests.get('https://www.baidu.com', timeout=0.1)
            return r.text
        except requests.Timeout:
            print('超时')


if __name__ == '__main__':
    while True:
        reques()
