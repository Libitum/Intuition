""" --- Config of Plod.py --- """
import web

#Configuration for Blog User, just google account
ACCOUNT = "libitum.zju@gmail.com"

#Configuration for database
DB_TYPE = "mysql"
DB_HOST = "r3139libitum.mysql.aliyun.com"
DB_PORT = 3306
DB_USER = "r8338libitum"
DB_PASSWORD = "ra633728b"
DB_DATABASE = "r8338libitum"

CACHE = False

#Configuration for web.py
web.config.debug = True
