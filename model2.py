# ^-^ coding: utf-8 ^-^
import web
import config

db = web.database(dbn=config.DB_TYPE, host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, pw=config.DB_PASSWORD, db=config.DB_DATABASE)

class Posts:
    __where = "post_type='"
    def __init__(self, tp):
        self.__where += tp + "'"

    def gets(self, order="id DESC", limit=10, offset=0):
        return db.select('in_posts', where=self.__where, order=order, limit=limit, offset=offset)
