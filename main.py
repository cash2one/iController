#!/usr/bin/env python

'''
    -------Adirects-------
    Create: Yuanji
    Date: 2015/11/08
    Fun: User FreqController
    -----------------
'''

import os, sys
import time
import json
import socket
import struct
from setting import *
from datetime import datetime
from collections import defaultdict
from multiprocessing import Process
from utils.log import LOG
from corebase.userfrequency import *
from corebase.statuscontroller import *


def daemonize():
    pid = os.fork()
    if pid < 0:
        os._exit(1)
    if pid > 0:
        os._exit(0)

    os.umask(0)
    os.setsid()

    pid = os.fork()
    if pid < 0:
        os._exit(1)
    if pid > 0:
        os._exit(0)

    for i in range(0,100):
        try:
            os.close(i)
        except Exception, e:
            pass
    file('/dev/null','r')
    file('/dev/null','a+')
    file('/dev/null','a+')


def start_user_frequency_collect():
    s = BrocastSocket()
    pro = list()
    for i in xrange(HANDLER_NUMBER):
        pro.append(Process(target = freqcontroller, args=(s,)))

    for i in xrange(HANDLER_NUMBER):
        pro[i].start()

    for i in xrange(HANDLER_NUMBER):
        pro[i].join()
    

def start_order_check_controller():
    HANDLER_NUMBER = 1
    pro = list()
    for i in xrange(HANDLER_NUMBER):
        pro.append(Process(target = ordercheckcontroller, args=()))

    for i in xrange(HANDLER_NUMBER):
        pro[i].start()

    for i in xrange(HANDLER_NUMBER):
        pro[i].join()



def start_order_status_controller():
    s = 0
    HANDLER_NUMBER = 1
    pro = list()
    for i in xrange(HANDLER_NUMBER):
        pro.append(Process(target = statuscontroller, args=(s,)))

    for i in xrange(HANDLER_NUMBER):
        pro[i].start()

    for i in xrange(HANDLER_NUMBER):
        pro[i].join()

def start():
    pro = list()

    # freqcontroller
    #print 'start user frequency collect...'
    #s = BrocastSocket()
    #for i in xrange(HANDLER_NUMBER):
    #    pro.append(Process(target = freqcontroller, args=(s,)))

    # order check
    print 'start order status check...'
    pro.append(Process(target = ordercheckcontroller, args=()))

    # realtime order status
    ''''''

    for p in pro:
        p.start()

    for p in pro:
        p.join()
if __name__ == '__main__':

    #daemonize()
    #start_user_frequency_collect()
    #start_order_check_controller()
    #start_order_status_controller()
    start()



