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

        user = web.cookies(author='', email='', url='')
        return render.article(article, comments, num, user)

    def POST(self, id):
        data = web.input()
        if(data.author == '' or data.email == '' or data.comment == ''):
            return 'author or email required.'

        web.setcookie('author', data.author)
        web.setcookie('email', data.email)
        web.setcookie('url', data.url)
        
        db_comment = model.Comments()
        db_comment.insert(id, data.author, data.email, data.url, web.ctx.ip, data.comment)

        return self.GET(id)

class Index:
    def GET(self):
        db_post = model.Posts()
        posts = db_post.gets(where='cat_id!=2')
        return render.articles(posts, None)

class Category:
    def GET(self, slug):
        db_post = model.Posts()
        db_terms = model.Terms()

        term_id = db_terms.get_term_id(slug)[0].term_id
        posts = db_post.gets(where='term_id=%s' % term_id)
        return render.articles(posts, None)

class Page(Article):
    pass

### Functions used in templates
def get_cat_list():
    db_term = model.Terms()
    return db_term.get_cat_list()

def get_page_list():
    db_post = model.Posts()
    return db_post.get_page_list()

def get_special_list(cat_id = None, num=7):
    if cat_id == None:
        #TODO 读取数据库里的配置
        cat_id = 2

    db_post = model.Posts()
    return db_post.get_special_list(cat_id, num)
    

def get_new_list(cat_id=0, num=7):
    db_post = model.Posts()
    return db_post.get_new_list(cat_id, num)

def get_top_views_list(cat_id=0, num=7):
    db_post = model.Posts()
    return db_post.get_top_views_list(cat_id, num)

def get_recent_comments_list(num=5):
    db_comment = model.Comments()
    return db_comment.get_recent_comments_list(num)

def get_link_list():
    pass

def get_tags_by_article():
    pass
