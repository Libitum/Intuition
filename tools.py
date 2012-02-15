# ^-^ coding: utf-8 ^-^
"""
Some functions for common
@version: $Id$
@author: Libitum<libitum@msn.com>
"""
import time

def getTime():
    return int(time.time())

def str2time(s, format="%Y-%m-%d %H:%M"):
    '''string format could be "%Y-%m-%d %H:%M"'''
    ts = time.strptime(s, format)
    return int(time.mktime(ts))

def time2str(t, format="%Y-%m-%d %H:%M"):
    '''string format could be "%Y-%m-%d %H:%M"'''
    ts = time.localtime(t)
    return time.strftime(format, ts)

if __name__ == "__main__":
    t = getTime()
    s = time2str(t)
    print t
    print s
    print str2time(s)

