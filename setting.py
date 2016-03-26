#!/usr/bin/env python
# coding=utf-8
'''
    Create: Yuanji
    Date:  2015/11/05

'''

HANDLER_NUMBER = 5

MCAST_GRP = '238.2.20.128' 
MCAST_PORT = 14333

''' frequency '''
FREQ_REDIS = (('192.168.167.92', 10501) , ('192.168.167.93', 10501))
''' order config '''
CONFIG_REDIS = (('08dce178449f48fb.m.cnbja.kvstore.aliyuncs.com', 6379), )
''' order realtime info '''
STATUS_REDIS = (('08dce178449f48fb.m.cnbja.kvstore.aliyuncs.com', 6379), )
STATUS_REDIS_PASS = "08dce178449f48fb:MtqweBNM789"

''' Order Status '''
STATUS_OK = '20'
STATUS_DAY_BUDGET = '21'
STATUS_NO_THIS_HOUR = '22'
STATUS_HOUR_BUDGET = '23'
STATUS_NO_TODAY_RANGE = '24'
STATUS_ADV_NO_MONEY = '25'
STATUS_ERROR = '30'
