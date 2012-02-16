# ^-^ coding: utf-8 ^-^
"""
Handle all operation from blog.
@version: $Id$
@author: Libitum<libitum@msn.com>
"""
import web

import model
from config import CONFIG
from tools import *
from plugins import *


### App initialization
blog = web.application(CONFIG['URL_MAPPING'], locals())

### Templates initialization
render = web.template.render('themes/imbalance', base="base", globals=locals())

### Parent handler
class Article:
    '''Parent class for article'''
    _data = {}
    _comments = {}
    def GET(self):
        return render.article(self._data, self._comments)

class Articles:
    '''Parent class for articles'''
    def get_data(self):
        pass

    def get_page(self):
        pass

    def GET(self):
        __data = self.get_data()
        __page = self.get_page()
        return render.articles(__data, __page)

### Main handler
class Index(Articles):
    def get_data(self):
        db_post = model.Posts()
        return db_post.gets()

### Functions used in templates
def get_nav_list():
    pass

def get_special_list():
    pass

def get_new_list():
    pass

def get_top_views_list():
    pass

def get_comment_list():
    pass

def get_link_list():
    pass

def get_tags_by_article():
    pass
