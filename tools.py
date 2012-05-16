# ^-^ coding: utf-8 ^-^
"""
Some functions for common
@version: $Id$
@author: Libitum<libitum@msn.com>
"""
import time
import hashlib
from config import CONFIG

def getTime():
    return int(time.time())

def str2time(s, format="%Y-%m-%d %H:%M:%S"):
    '''string format could be "%Y-%m-%d %H:%M:%S"'''
    ts = time.strptime(s, format)
    return int(time.mktime(ts))

def time2str(t, format="%Y-%m-%d %H:%M"):
    '''string format could be "%Y-%m-%d %H:%M"'''
    ts = time.localtime(t)
    return time.strftime(format, ts)

def get_abstract(article):
    return article.split('<!--more-->', 1)[0]

def get_gravatar(email, size=48):
    m = hashlib.new('md5', email).hexdigest()
    return "http://0.gravatar.com/avatar/%s?s=%s&d=identicon&r=G" % (m, size)

def __get_url(tp, char):
    url = None
    um = CONFIG['URL_MAPPING']
    for i in range(1, len(um), 2):
        if um[i] == tp:
            url = um[i-1].replace(r'(.+)', str(char))
            break
    return url

def get_blog_url(char):
    return __get_url('Article', char)

def get_cat_url(char):
    return __get_url('Category', char)

def get_tag_url(char):
    return __get_url('Tag', char)

def get_page_url(char):
    return __get_url('Page', char)

if __name__ == "__main__":
    '''
    t = getTime()
    s = time2str(t)
    print t
    print s
    print str2time(s)
    '''
    get_blog_url(123)

