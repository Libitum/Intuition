# ^-^ coding: utf-8 ^-^
import web
import config

class DB:
    __db = web.database(dbn=config.db_type, user=config.db_user, pw=config.db_password, db=config.db_database)
