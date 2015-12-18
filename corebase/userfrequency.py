#!/usr/bin/env python
# coding=utf-8


import os, sys
import traceback
try:
    path = os.getcwd()
    parent_path  = os.path.dirname(path)
    sys.path.append(parent_path)
except Exception,e:
    print "userfrequency:%s" % e
import time
import json
import socket
import struct
from setting import *
from datetime import datetime
from collections import defaultdict
from multiprocessing import Process
from corebase.database import Database
from utils.log import LOG

log = LOG()

def BrocastSocket():
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(('',MCAST_PORT))
    mreq=struct.pack("=4sl",socket.inet_aton(MCAST_GRP),socket.INADDR_ANY)
    s.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,mreq)
    return s

def freqcontroller(sock):
    rdb = Database(FREQ_REDIS)
    while 1:
        #time.sleep(1)
        try:
            info = sock.recv(1024)
            #log.debug(info)
            #'''
            info = json.loads(info)
            if info.has_key("userid"):
                userid = info['userid']
            if info.has_key("league"):
                adxid = info['league']
            if info.has_key("pid"):
                pid = info['pid']
            if info.has_key("execid"):
                execid = info['execid']

            rdb.incUserHourPv(userid, execid, adxid)
            rdb.incUserDayPv(userid, execid, adxid)
            rdb.incPidPv(pid, execid)
            #'''
        except Exception, e:
            print e
            pass

