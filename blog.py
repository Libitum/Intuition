# ^-^ coding: utf-8 ^-^
"""
Handle all operation from blog.
@version: $Id$
@author: Libitum<libitum@about.me>
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
    def GET(self, id):
        db_post = model.Posts()
        article = db_post.get(id)[0]
        comments = {}
        return render.article(article, comments)

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
        #datas = db_post.gets()
        #articles = []
        return db_post.gets(where='cat_id!=2')

### Functions used in templates
def get_cat_list():
    db_term = model.Terms()
    return db_term.getCatList()

def get_page_list():
    db_post = model.Posts()
    return db_post.getPageList()

def get_special_list(cat_id = None, num=7):
    if cat_id == None:
        #TODO 读取数据库里的配置
        cat_id = 2

    db_post = model.Posts()
    return db_post.getSpecialList(cat_id, num)
    

def get_new_list(cat_id=0, num=7):
    db_post = model.Posts()
    return db_post.getNewList(cat_id, num)

def get_top_views_list(cat_id=0, num=7):
    db_post = model.Posts()
    return db_post.getTopViewsList(cat_id, num)

def get_comment_list():
    pass

def get_link_list():
    pass

def get_tags_by_article():
    pass
