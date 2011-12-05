""" --- Config of Plod.py --- """
import web

#Configuration for Blog User, just google account
ADMIN = "libitum.zju@gmail.com"

#Configuration for database
DB_TYPE = "MYSQL"
DB_HOST = "LOCALHOST"
DB_USER = "LIBITUM"
DB_PASSWORD = "LIBITUM"
DB_DATABASE = ""

CACHE = False

#Configuration for web.py
web.config.debug = True
