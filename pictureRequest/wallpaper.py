import re

if __name__ == '__main__':
    url = 'http://mgzwl.cooco.net.cn/testdetail/480081/'
    group = re.search(r'(\S+)://(\S+)/(\S+)/(\d+)', url)
    print(group.group())
    print(group.group(1))
    print(group.group(2))
    print(group.group(3))
    print(group.group(4))

    # url = url.replace(now, '888888')
    # print(url)
