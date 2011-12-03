#!/usr/bin/env python
# ^-^ coding: utf-8 ^-^
import web
urls = (
    "", "reload",
    "/(.*)", "index"
)

class reload:
    def GET(self):
        web.seeother('/')

class index:
    def GET(self, path):
        return "hello " + path

admin = web.application(urls, locals())
