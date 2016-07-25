# -*- coding: utf-8 -*-

from redis import Redis

conn = Redis(host='127.0.0.1', port='6379', db=11, password='')


# hash
conn.hmget('hkey', ['k1', 'k2'])
conn.hset('hkey', {'k1': 'v1', 'k2': 'v2'})
conn.hdel('hkey', 'k2', 'k3')
conn.hlen('hkey')
conn.hexists('hkey', 'key')
conn.hkeys('hkey')
conn.hvals('hkey')
conn.hgetall('hkey')
conn.hincrby('hkey', 'key', 1)
conn.hincrbyfloat('hkey', 'key', 2.3)

# list
conn.rpush('lkey', 1, 2, 3)
conn.lpush('lkey', 1, 2, 3)
conn.lpop('lkey')
conn.rpop('lkey')
conn.lrange('lkey', 0, -1) # return a list
conn.lindex('lkey', 2)
conn.ltrim('lkey', 1, -1)
conn.blpop(['list1', 'list2'], 1)
conn.brpop(['list1', 'list2'], 2)
conn.rpoplpush('list1', 'list2')
conn.brpoplpush('list1', 'list2', 3)

# set
conn.sadd('key', 'item1', 'item2')
conn.srem('key', 'item2')
conn.ismember('key', 'item') # not sure
conn.scard('key')
conn.smembers('key')
conn.smove('key1', 'key2', 'item')
conn.sdiff('key1', 'key2', 'key3') # 返回存在第一个集合，不在其他集合的元素
conn.sinter('key1', 'key2')
conn.sunion('key1', 'key2',)

# string
conn.set('key', '15')
conn.get('key')
conn.incr('key') # conn.incr('key', 1)
conn.incr('key', 5)
conn.decr('key', 5)
conn.incrbyfloat('key')
conn.incrbyfloat('key', -4.5)
conn.append('key', ' world')
conn.substr('key', 0, -2)
conn.setrange('key', 11, ' world!')

# zset
conn.zadd('zkey', 'member', 10, 'member1', 20)
conn.zrem('zkey', 'member1')
conn.zcard('zkey')
conn.zincrby('zkey', 'member', 10)
conn.zcount('zkey', 10, 20)
conn.zrank('zkey', 'member') # 分值从小到大排列
conn.zscore('zkey', 'member')
conn.zrange('zkey', 0, 9, withscores=True) # 返回前10名的成员和分数
conn.zinterstore('zset-u', ['zset1', 'zset2'], aggregate='sum') # 成员的交集，聚合函数默认为sum，成员排名相加后为新的排名
conn.zunionstore('zset-u', ['zset1', 'zset2'], aggregate='min') # 成员的并集，聚合函数为min取最小值为新的排名

