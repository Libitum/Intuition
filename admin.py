# ^-^ coding: utf-8 ^-^
import web
urls = (
    "/(.*)", "Index"
)

class Index:
    def GET(self, path):
        return "hello " + path + " in admin"

admin = web.application(urls, locals())
