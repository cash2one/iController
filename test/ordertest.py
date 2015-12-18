#!/usr/bin/env python
# coding=utf-8

import os,sys
try:
    os.chdir(os.path.dirname(sys.argv[0]))
    path = os.getcwd()
    parent_path  = os.path.dirname(path)
    sys.path.append(parent_path)
except Exception,e:
    print e

import corebase
from corebase.coreorder import CoreOrder
from corebase.coreorder import CoreOrderThread


if __name__ == '__main__':
    ord = CoreOrder()
    c_order = CoreOrderThread(ord)
    c_order.start()
