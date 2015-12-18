#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import redis
from collections import defaultdict
from datetime import datetime
from time import localtime,strftime


class RedisDb(object):
    def __init__(self, host, port):
        self.r = redis.StrictRedis(host = host, port = port, db=0)

    def _get(self, key):
        return self.r.get(key)

    def _hkeys(self, key):
        return self.r.hkeys(key)

    def _set(self, key, value):
        return self.r.set(key, value)

    def _expireat(self, key, tm):
        return self.r.expireat( key, tm )

    def _expire(self, key, tm):
        return self.r.expire( key, tm )

    def _incr(self, key):
        return self.r.incr(key)    

    def _hkeys(self, key):
        return self.r.hkeys(key)    

    def _incrbyfloat(self, key, num):
        return self.r.incrbyfloat(key, num)

    def _decbyfloat(self, key, num):
        return self.r.incrbyfloat(key, num)

    def _hgetall(self, key):
        return self.r.hgetall(key)

    def _hget(self, key, field):
        return self.r.hget(key, field)
    
    def _hset(self, key, field, value):
        return self.r.hset(key, field, value)

    def _hincr(self, key, field):
        return self.r.hincrby(key, field)

    def _incrby(self, key, num):
        return self.r.incrby(key, int(num))

    def _hincrby(self, key, field, num):
        return self.r.hincrby(key, field, int(num)) 

    def _hincrbyfloat(self, key, field, num):
        return self.r.hincrbyfloat(key, field, float(num)) 

