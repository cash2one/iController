#!/usr/bin/env python
# coding=utf-8

import logging

LOGLEVEL = logging.DEBUG#DEBUG/INFO/WARNNING/ERROR

def LOG():
    LOG_FILENAME_ACCEPT = 'accept.log'
    FORMAT = "%(asctime)s %(levelname)-8s %(message)s"
    #FORMAT = ""
    logging.basicConfig(
        filename=LOG_FILENAME_ACCEPT, 
        level=LOGLEVEL, 
        format=FORMAT
        )
    log = logging.getLogger('accept')
    return log
