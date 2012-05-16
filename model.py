# ^-^ coding: utf-8 ^-^
import web
import tools
from config import CONFIG

DB = CONFIG['DB']
db = web.database(dbn=DB['TYPE'], host=DB['HOST'], port=DB['PORT'], 
        user=DB['USER'], pw=DB['PASSWORD'], db=DB['DATABASE'])

class Posts:
    __vars = {}
    def __init__(self, tp = 'post'):
        self.__vars['type'] = tp

    def gets(self, order="id DESC", limit=10, offset=0, where=None):
        self.__vars['limit'] = limit
        self.__vars['offset'] = offset
        where = 'where ' + where if where is not None else ''
        query = "SELECT `id`, `post_title`, `post_content`, `post_date`, `post_status`, \
                `post_views`, `comment_count`, `name`, `slug`\
                FROM in_posts \
                LEFT JOIN in_terms ON `cat_id` = `term_id` %s\
                ORDER BY id DESC LIMIT $limit OFFSET $offset;" % where
        return db.query(query, vars=self.__vars)

    def get(self, id):
        self.__vars['id'] = id
        return db.select('in_posts', where="id=$id or post_slug=$id", limit=1, vars=self.__vars)

    def update(self, id, data):
        self.__vars['id'] = id
        timestr = data['year'] + '-' + data['month'] + '-' + data['day'] + ' ' + data['hour'] + ':' + data['min']
        post_date = tools.str2time(timestr)
        return db.update('in_posts', where="id=$id", vars=self.__vars, 
                cat_id=data['cat_id'], post_title=data['post_title'],
                post_content=data['post_content'], post_slug=data['post_slug'], 
                post_status=data['post_status'], post_date=post_date
                )

    def insert(self, data, tp='post'):
        timestr = data['year'] + '-' + data['month'] + '-' + data['day'] + ' ' + data['hour'] + ':' + data['min']
        post_date = tools.str2time(timestr)
        t = db.transaction()
        try:
            db.query("UPDATE in_terms SET num = num+1 WHERE term_id=" + data['cat_id'])
            db.insert('in_posts', cat_id=data['cat_id'], post_title=data['post_title'],
                post_content=data['post_content'], post_slug=data['post_slug'], 
                post_status=data['post_status'], post_date=post_date, 
                post_type=tp
                )
        except:
            t.rollback()
            return False
        else:
            t.commit()
            return True

    def delete(self, id):
        self.__vars['id'] = id
        return db.delete('in_posts', where='id=$id', vars=self.__vars)

    def getPageList(self):
        return db.select('in_posts', what="post_title, post_slug", where='post_type="page"')
    
    def getNewList(self, cat_id=0, num=7):
        return db.select('in_posts', what="id, post_title", where='cat_id!=%d' % cat_id,
                limit=num, order="post_date DESC")

    def getSpecialList(self, cat_id, num=7):
        return db.select('in_posts', what="id, post_title", where="cat_id=%d" % cat_id, 
                limit=num, order="post_date DESC" )

    def getTopViewsList(self, cat_id, num=7):
        return db.select('in_posts', what="id, post_title, post_views", where="cat_id!=%d" % cat_id, 
                limit=num, order="post_views DESC" )

class Terms:
    def __init__(self):
        pass

    def gets(self, tag=0):
        return db.select('in_terms', where="tag=$tag", vars={'tag' : tag})

    def getTags(self, id):
        query = "SELECT name FROM in_terms, in_term_post WHERE in_term_post.post_id = $id \
                AND in_term_post.term_id = in_terms.term_id;"
        return db.query(query, {'id' : id})

    def getSuggestTags(self):
        return db.select('in_terms', what="name", where="tag=1", order="num DESC")

    def getAllTags(self):
        query = "SELECT name, num FROM in_terms WHERE tag=1;"
        return db.query(query)

    def getCatList(self):
        return db.select('in_terms', what="name, slug", where="tag=0")

    def getTermId(self, slug):
        return db.select('in_terms', what='term_id', where="slug=$slug", limit=1, vars={'slug':slug})

class Comments:
    def get_all(self, limit=10, offset = 0):
        query = "SELECT comment_author, comment_author_email, comment_author_url, \
                comment_author_IP, comment_date, comment_content, post_title \
                FROM in_comments \
                LEFT JOIN in_posts ON comment_post_id=id ;"
        return db.query(query)

    def gets(self, post_id):
        return db.select('in_comments', where="comment_post_id=%s" % post_id)

    def getRecentCommentsList(self, num):
        return db.select('in_comments', what="comment_id, comment_post_id, comment_author, comment_author_email, comment_content",
                limit=num, order="comment_date DESC" )

    def insert(self, post_id, author, email, url, ip, comment):
        return db.insert('in_comments', comment_post_id=post_id, comment_author=author, comment_author_email=email, comment_author_url=url, comment_author_IP=ip, comment_date=tools.getTime(), comment_content=comment)
