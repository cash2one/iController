#!/usr/bin/env python
# coding=utf-8

import time
import json
import threading
from setting import *
from database import Database
from datetime import datetime
from collections import defaultdict
from utils.log import LOG


log = LOG()

TYPE_CPM = 1
TYPE_CPC = 2
TYPE_HOUR_SHARE = 1
TYPE_HOUR_SHARE_NO = 0


#STATUS_OK_LIST = [STATUS_OK, STATUS_DAY_BUDGET, STATUS_NO_THIS_HOUR, ]
WEEK_MAP = [1,2,3,4,5,6,0]

MATERIAL_MAP = {
    1:'img',
    2:'img',
    3:'img',
    4:'mv',
    5:'flash',
    6:'flash',
    7:'mv',
}

class CoreOrder(threading.Thread):
    def __init__(self):
        '''
            OrderObject: { "execID":{"adverID":xxx, "bidtype":1/2,"hourshare":True/False, "hourlist":[x,x,x,x], "budget":xxx}  }
        '''
        threading.Thread.__init__(self)
        self.m_Flag = 1
        self.m_OrderOb = None
        self.db = Database(CONFIG_REDIS)
        self.m_OrderOb_A = defaultdict()
        self.m_OrderOb_B = defaultdict()
        ''' init '''
        self.today = datetime.now().day
        self.timestamp = self.db.getOrderConfigStamp()
        self.coreProcess(self.m_OrderOb_A)

    def choose(self):
        if self.m_Flag == 1:
            self.m_OrderOb = self.m_OrderOb_A
        elif self.m_Flag == 2:
            self.m_OrderOb = self.m_OrderOb_B
 
    def reload(self):
        # clear
        self.clear()
        # load
        if self.m_Flag == 1:
            self.coreProcess(self.m_OrderOb_B)
        elif self.m_Flag == 2:
            self.coreProcess(self.m_OrderOb_A)
        # change
        self.change()

    def change(self):
        if self.m_Flag == 1:
            self.m_Flag = 2
        elif self.m_Flag == 2:
            self.m_Flag = 1

    def clear(self):
        if self.m_Flag == 1:
            self.m_OrderOb_B.clear()
        elif self.m_Flag == 2:
            self.m_OrderOb_A.clear()

    def parser(self, info):
        try:
            return json.loads(info)
        except Exception,e:
            print 'parser:%s' % e

    def getOrderRealList(self):
        try:
            re = list()
            self.choose()
            return self.m_OrderOb.keys()
        except Exception, e:
            print 'getOrderRealList:%s' %  e
            return re


    def getOrderRealInfo(self, execID):
        try:
            self.choose()
            if self.m_OrderOb.has_key(execID):
                return self.m_OrderOb[execID]
            else:
                return None
        except Exception, e:
            print 'getOrderRealInfo:%s' %  e

    def setOrderCreateDetail(self, order):
        if order.has_key("create"):
            create_list = order['create']
            if len(create_list) > 0:
                for c in create_list:
                    if c.has_key('material'):
                        mat_list = c['material']
                        for m in mat_list:
                            mat = defaultdict()
                            if m.has_key('cid'):
                                mat['cid'] = str(m['cid'])
                            if m.has_key('width'):
                                mat['width'] = str(m['width'])
                            if m.has_key('height'):
                                mat['height'] = str(m['height'])
                            if m.has_key('format'):
                                format = m['format']
                                if MATERIAL_MAP.has_key(format):
                                    format = MATERIAL_MAP[format]
                                else:
                                    format = 'img'
                                mat['type'] = format
                            if m.has_key('destination_url'):
                                mat['c_url'] = m['destination_url']
                            if m.has_key('material_url'):
                                mat['m_url'] = m['material_url']
                            if m.has_key('monitor_url'):
                                monitor_url_list = m['monitor_url']
                                if len(monitor_url_list) > 0:
                                    monitor_url = monitor_url_list[0]
                                    mat['monitor_url'] = monitor_url

                            if mat['cid'] and mat['width'] and mat['height']:
                                detail = json.dumps(mat)
                                self.db.setCreateInfo(mat['cid'], detail )
                                log.debug(detail)


 
    def getOrderAdvertiser(self, order):
        if order.has_key("order"):
            ord = order['order']
            adverID = ord['advertiser']
            return adverID

    def getOrderBidType(self, order):
        if order.has_key("order"):
            ord = order['order']
            type = int(ord['target_price_type'])
            if type == TYPE_CPM:
                return TYPE_CPM
            if type == TYPE_CPC:
                return TYPE_CPC

    def getOrderHourShare(self, order):
        if order.has_key("order"):
            ord = order['order']
            hourshare = int(ord['hour_share'])
            if hourshare == TYPE_HOUR_SHARE:
                return True
            if hourshare == TYPE_HOUR_SHARE_NO:
                return False

    def parseOrderEndTime(self, order):
        if order.has_key("range"):
            range = order["range"]
            if range.has_key("end"):
                return range["end"]

    def parseOrderTodayRange(self, order):
        # 0:week1 
        today_week = int(datetime.now().weekday())
        today_week = WEEK_MAP[today_week]
        if order.has_key("range"):
            range = order["range"]
            if range.has_key("week"):
                w = range['week']
                for week in w:
                    day = int(week['weekday'])
                    budget = week['budget']
                    hourlist = week['hour']
                    if day == today_week:
                        return day, budget, hourlist
        return None, None, None

    def dealOrderExpire(self, endtime):
        # True: Out of date
        # False: In Range
        if not endtime:
            return False

        now = datetime.now()
        stringtime = "%s-%s-%s 23:59:59" % (now.year, now.month, now.day)
        today = time.strptime(stringtime, "%Y-%m-%d %H:%M:%S")
        todaytm = int(time.mktime(today))

        endday = "%s 23:59:59" % endtime
        endday = time.strptime(endday, "%Y-%m-%d %H:%M:%S")
        endtm = int(time.mktime(endday))

        if endtm < todaytm:
            return True
        else:
            return False

    def dealOrderHourList(self, hourlist):
        now_hour = int(datetime.now().hour)
        for h in hourlist:
            if int(h) == now_hour:
                return True
        return False

    def printOrderOb(self, pOrderObject):
        count = 0
        for k,v in pOrderObject.iteritems():
            log.info( "%s->%s" % (k,v) )
            count = count + 1
        log.info( "Total:%d" % count )

    def coreProcess(self, pOrderObject):
        order_list = self.db.getOrderList()
        if not order_list:
            return
        for ord in order_list:
            info = self.db.getOrderInfo(ord)
            info = self.parser(info)
            endday = self.parseOrderEndTime(info)
            if self.dealOrderExpire(endday):
                pass
                # delete order
            else:
                weekday, budget, hourlist = self.parseOrderTodayRange(info)
                if weekday is None:
                    # set no today range
                    self.db.setOrderStatus(ord, STATUS_NO_TODAY_RANGE)
                if hourlist:
                    if not self.dealOrderHourList(hourlist):
                        # set no hour
                        self.db.setOrderStatus(ord, STATUS_NO_THIS_HOUR)

                advertiser = self.getOrderAdvertiser(info)
                bidtype    = self.getOrderBidType(info)
                hourshare  = self.getOrderHourShare(info)
                #self.setOrderCreateDetail(info)
                '''
                    OrderObject: { "execID":{"adverID":xxx, "bidtype":1/2,"hourshare":True/False, "hourlist":[x,x,x,x], }  }
                '''
                orderdata = { \
                    'adverID':advertiser,\
                    'bidtype':bidtype, \
                    'hourshare':hourshare, \
                    'budget':budget, \
                    'hourlist':hourlist,}

                pOrderObject[ord] = orderdata

        self.printOrderOb(pOrderObject)
                

    def newConfigureMonitor(self):
        try:
            # timestamp change
            tm = self.db.getOrderConfigStamp()
            if tm != self.timestamp:
                self.timestamp = tm
                log.info('CoreOrder: New Configuration & Reload OK!')
                return True

            # day change
            da = datetime.now().day 
            if da != self.today:
                self.reload()
                self.today = da
                log.info('CoreOrder: Happy New Day & Reload OK!')
                return True

            return False
        except Exception, e:
            log.error("newConfigureMonitor:%s" % e)
            return False


    def run(self):
        while True:
            try:
                time.sleep(0.1)
                if self.newConfigureMonitor():
                    self.reload()
                    
            except Exception, e:
                log.error("CoreOrder:%s" % e)
                continue

class CoreOrderThread(threading.Thread):
    def __init__(self, OrderObject):
        threading.Thread.__init__(self)
        self.ord = OrderObject

    def run(self):
        while True:
            try:
                time.sleep(10)
                self.ord.reload()
            except Exception, e:
                log.error(e)



