import redis

if __name__ == '__main__':
    r = redis.Redis(host='139.159.134.78', port=16379, password='m6ojIOg1rvcc5go8', db=0)

    # r.set('baozitest', 'niubi')
    # print(r.get('baozitest'))
    # r.delete('baozitest')
    # r.flushall('user_cf_buy_rec',)
    print(r.hgetall('user_cf_buy_rec'))
