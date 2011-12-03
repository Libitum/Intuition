# ^-^ coding: utf-8 ^-^
import web
urls = (
    "/blog/(.+)\.html", "Article",
    "/cat/(.+)", "Category",
    "/tag/(.+)", "Tag",
    "/(.*)", "Index"
)

class Index:
    def GET(self, path):
        return "hello " + path + " in blog"

blog = web.application(urls, locals())
