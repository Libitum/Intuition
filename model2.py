# ^-^ coding: utf-8 ^-^
import web
import config
import tools

db = web.database(dbn=config.DB_TYPE, host=config.DB_HOST, port=config.DB_PORT, 
        user=config.DB_USER, pw=config.DB_PASSWORD, db=config.DB_DATABASE)

class Posts:
    __vars = {}
    def __init__(self, tp = 'post'):
        self.__vars['type'] = tp

    def gets(self, order="id DESC", limit=11, offset=0):
        self.__vars['limit'] = limit
        self.__vars['offset'] = offset
        query = "SELECT `id`, `post_title`, `post_date`, `post_status`, `post_views`, `comment_count`, `name` \
                FROM in_posts \
                LEFT JOIN in_terms ON `cat_id` = `term_id` \
                ORDER BY id DESC LIMIT $limit OFFSET $offset;"
        return db.query(query, vars=self.__vars)

    def get(self, id):
        self.__vars['id'] = id
        return db.select('in_posts', where="id=$id", vars=self.__vars)

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

class Comments:
    def gets(self, limit=10, offset = 0):
        query = "SELECT comment_author, comment_author_email, comment_author_url, \
                comment_author_IP, comment_date, comment_content, post_title \
                FROM in_comments \
                LEFT JOIN in_posts ON comment_post_id=id ;"
        return db.query(query)

