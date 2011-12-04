# ^-^ coding: utf-8 ^-^
import web
import config

db = web.database(dbn=config.db_type, host=config.db_host, user=config.db_user, pw=config.db_password, db=config.db_database)
