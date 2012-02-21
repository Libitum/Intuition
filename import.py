# ^-^ coding: utf-8 ^-^
'''
这个只是临时用用，以后再整合
'''
from xml.dom import minidom
from model import db
from tools import *
dom = minidom.parse("wordpress.xml")

#do sth with category
cats = dom.getElementsByTagName('wp:category')
datas = []
for cat in cats:
    c = {}
    for node in cat.childNodes:
        if node.nodeName == 'wp:category_nicename':
            c['slug'] = node.firstChild.nodeValue
        elif node.nodeName == 'wp:cat_name':
            c['name'] = node.firstChild.nodeValue

    datas.append(c)

for data in datas:
    db.insert('in_terms', name=data['name'], slug=data['slug'], tag=0, num=0)

#do sth with tag
tags = dom.getElementsByTagName('wp:tag')
datas = []
for tag in tags:
    c = {}
    for node in tag.childNodes:
        if node.nodeName == 'wp:tag_slug':
            c['slug'] = node.firstChild.nodeValue
        elif node.nodeName == 'wp:tag_name':
            c['name'] = node.firstChild.nodeValue

    datas.append(c)

for data in datas:
    db.insert('in_terms', name=data['name'], slug=data['slug'], tag=1, num=0)


#do sth with posts
items = dom.getElementsByTagName('item')

for item in items:
    data = {'comments' : [], 'tag':None, 'views':0}
    for node in item.childNodes:
        if node.nodeName == 'title':
            data['title'] = node.childNodes[0].data

        elif node.nodeName == 'wp:post_id':
            data['post_id'] = node.childNodes[0].data

        elif node.nodeName == 'content:encoded':
            #data['post_content'] = node.childNodes[0].data
            if node.firstChild == None:
                data['post_content'] = ''
            else:
                data['post_content'] = node.firstChild.nodeValue

        elif node.nodeName == 'wp:post_date':
            data['post_date'] = node.childNodes[0].data

        elif node.nodeName == 'wp:post_type':
            data['post_type'] = node.childNodes[0].data

        elif node.nodeName == 'category':
            if node.getAttribute('domain') == 'category':
                data['cat'] = node.childNodes[0].data
            elif node.getAttribute('domain') == 'post_tag':
                if data['tag'] == None:
                    data['tag'] = []
                data['tag'].append(node.firstChild.nodeValue)

        elif node.nodeName == 'wp:postmeta':
            meta = node.childNodes
            if meta[1].nodeName == 'wp:meta_key' and meta[1].childNodes[0].data == 'views':
                data['views'] = meta[3].childNodes[0].data

        elif node.nodeName == 'wp:comment':
            if node.childNodes == None:
                continue
            comment = {}
            for meta in node.childNodes:
                if meta.nodeName == 'wp:comment_author':
                    comment['author'] = meta.firstChild.nodeValue

                elif meta.nodeName == 'wp:comment_author_email':
                    comment['email'] = meta.firstChild.nodeValue

                elif meta.nodeName == 'wp:comment_author_url':
                    if meta.firstChild == None:
                        comment['url'] = ''
                    else:
                        comment['url'] = meta.firstChild.nodeValue

                elif meta.nodeName == 'wp:comment_author_IP':
                    comment['ip'] = meta.firstChild.nodeValue

                elif meta.nodeName == 'wp:comment_date':
                    comment['date'] = meta.firstChild.nodeValue

                elif meta.nodeName == 'wp:comment_content':
                    comment['content'] = meta.firstChild.nodeValue

            data['comments'].append(comment)

    #insert database
    if data.has_key('cat'):
        cat = db.select('in_terms', what="term_id", where='name=$name', vars={'name' : data['cat']})
        cat_id = cat[0]['term_id']
        db.query('update in_terms set num=num+1 where term_id=%s' % cat_id)
    else:
        cat_id = 0

    post_id = data['post_id']
    db.insert('in_posts', id=data['post_id'], cat_id=cat_id, post_title=data['title'], 
            post_date=str2time(data['post_date']), post_content=data['post_content'], 
            post_slug='', post_status=1, post_type=data['post_type'], post_views=data['views'], 
            comment_count=0
            )
    #处理tags
    if data['tag'] is not None:
        for tag in data['tag']:
            t = db.select('in_terms', what="term_id", where='name=$name', vars={'name' : tag})
            t_id = t[0]['term_id']
            db.insert('in_term_post', term_id=t_id, post_id=post_id)
            db.query('update in_terms set num=num+1 where term_id=%s' % t_id)

    #处理评论
    for c in data['comments']:
        db.insert('in_comments', comment_post_id=post_id, comment_author=c['author'], 
                comment_author_email=c['email'], comment_author_url=c['url'], comment_author_IP=c['ip'], 
                comment_date=str2time(c['date']), comment_content=c['content'])

    db.update('in_posts', where='id=%s' % post_id, comment_count=len(data['comments']))



