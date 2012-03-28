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

### Main handler
class Article:
    '''Parent class for article'''
    def get_article(self, id):
        db_post = model.Posts()
        return db_post.get(id)[0]

    def get_comments(self, post_id):
        db_comment = model.Comments()
        return db_comment.gets(post_id)
    
    def GET(self, id):
        if id == 'favicon.ico':
            return None
        db_comment = model.Comments()

        article = self.get_article(id)
        comments = self.get_comments(article.id)
        num = len(comments)
        print comments
        return render.article(article, comments, num)

class Index:
    def GET(self):
        db_post = model.Posts()
        posts = db_post.gets(where='cat_id!=2')
        return render.articles(posts, None)

class Category:
    def GET(self, slug):
        db_post = model.Posts()
        db_terms = model.Terms()

        term_id = db_terms.getTermId(slug)[0].term_id
        posts = db_post.gets(where='term_id=%s' % term_id)
        return render.articles(posts, None)

class Page(Article):
    pass

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
