#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import traceback,json
from setting import  *
from utils.redisdb import RedisDb
from datetime import datetime
from time import localtime,strftime


class Database(object):
    def __init__(self, redis_conf, password = None):
        self.counter = 0
        self.red = None
        self.red_list = list()
        self.m_redis_conf = redis_conf
        self.hour = lambda : str(datetime.now().hour).zfill(2)
        self.today = lambda : strftime("%Y-%m-%d", localtime())
        self.initDatabase(password)

    def initDatabase(self, password):
        if isinstance(self.m_redis_conf, tuple):
            for r in self.m_redis_conf:
                try:
                    self.red_list.append( RedisDb(r[0],r[1],password=password ))
                except Exception, e:
                    print e

    def switch(self):
        #print self.red_list
        if self.counter < len(self.red_list):
            pass
        else:
            self.counter = 0
        self.red = self.red_list[self.counter]
        self.counter = self.counter + 1
    
    def expiretime(self):
        now = datetime.now()
        stringtime = "%s-%s-%s 23:59:59" % (now.year, now.month, now.day)
        tm = time.strptime(stringtime, "%Y-%m-%d %H:%M:%S")
        tm = int(time.mktime(tm))
        return tm

    def incUserHourPv(self, userid, eid, adx):
        try:
            if userid and eid and adx:
                self.switch()
                key = "user:pv:hour:%s:%s" %  (userid, adx)
                self.red._hincr(key, eid)
                self.red._expire(key, 3600)
        except Exception,e:
            print e

    def incUserDayPv(self, userid, eid, adx):
        try:
            if userid and eid and adx:
                self.switch()
                key = "user:pv:day:%s:%s" % ( userid, adx)
                self.red._hincr(key, eid)
                self.red._expireat(key, self.expiretime())
        except Exception,e:
            print e

    def incPidPv(self, pid, eid):
        try:
            if pid and eid:
                self.switch()
                key = "pid:pv:%s" % (pid,)
                self.red._hincr(key, eid)
                self.red._expireat(key, self.expiretime())
        except Exception,e:
            print e

    def getOrderList(self):
        try:
            self.switch()
            return self.red._hkeys("exec:raw")
        except Exception, e:
            print e

    def getOrderInfo(self, orderid):
        try:
            self.switch()
            return self.red._hget("exec:raw", orderid)
        except Exception, e:
            print e

    def setCreateInfo(self, cid, detail):
        try:
            self.switch()
            key_1 = "cid:detail:%s" % cid
            #key_2 = "cid:raw:%s" % self.today()
            self.red._set(key_1, detail)
            #self.red._hset(key_2, cid, detail)
        except Exception, e:
            print e

    def getAdvertiserMoney(self, advid):
        try:
            self.switch()
            money = self.red._get("adv:cash:%s" % advid)
            if money:
                return int(float(money))
            else:
                return 0
        except Exception, e:
            print "getAdvertiserMoney:%s" % e
            return 0

    def getAdvertiserTodaySpend(self, advid):
        try:
            self.switch()
            money = self.red._get("adv:%s:%s" % (self.today(),advid))
            if money:
                return int(float(money)/1000)
            else:
                return 0
        except Exception, e:
            print "getAdvertiserMoney:%s" % e
            return 0

    def getOrderTodayMoney(self, orid):
        # total money ,this hour money
        try:
            self.switch()
            hour = self.hour()
            real_money = self.red._hgetall("eid:hourspend:%s:%s" % (self.today(),orid))
            if real_money:
                havespend = hourspend = 0
                for tb in real_money.iteritems():
                    if tb[0] <= hour:
                        havespend = havespend + int(tb[1])/1000
                    if tb[0] == hour:
                        ''' hourspend '''
                        hourspend = int(tb[1])/1000
                return havespend, hourspend
            else:
                return 0, 0
        except Exception, e:
            print "getOrderTodayMoney:%s" % e
            return None, None

    def getOrderTodayClick(self, orid):
        # total click number
        try:
            self.switch()
            hour = self.hour()
            imp = self.red._hgetall("eid:click:%s:%s" % (self.today(), orid))
            if imp:
                haveclick = 0
                for tb in imp.iteritems():
                    if tb[0] <= hour:
                        haveclick = haveclick + int(tb[1])

                return haveclick
            else:
                return 0
        except Exception, e:
            print "getOrderTodayClick:%s" % e
            return 0

    def getOrderTodayShow(self, orid):
        # total show number
        try:
            self.switch()
            hour = self.hour()
            imp = self.red._hgetall("eid:show:%s:%s" % (self.today(),orid))
            if imp:
                haveshow = 0
                for tb in imp.iteritems():
                    if tb[0] <= hour:
                        haveshow = haveshow + int(tb[1])

                return haveshow
            else:
                return 0
        except Exception, e:
            print "getOrderTodayShow:%s" % e
            return 0

    def getOrderTodayResponse(self, orid):
        # total response number
        try:
            self.switch()
            hour = self.hour()
            imp = self.red._hgetall("exec:response:%s:%s" % (self.today(), orid))
            if imp:
                response = 0
                for tb in imp.iteritems():
                    if tb[0] <= hour:
                        response = response + int(tb[1])

                return response
            else:
                return 0
        except Exception, e:
            print "getOrderTodayResponse:%s" % e
            return 0

    def setOrderStatus(self, eid, status):
        #'''
        try:
            self.switch()
            return self.red._hset("exec:status", eid, status)
        except Exception, e:
            print "setOrderStatus:%r" % e
        #'''

    def getOrderConfigStamp(self):
        try:
            self.switch()
            return self.red._get("exec:timestamp")
        except Exception, e:
            print "getOrderConfigStamp:%r" % e
            return 0
