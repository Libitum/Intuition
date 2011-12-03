#!/usr/bin/env python
# ^-^ coding: utf-8 ^-^
import web
import admin

### Url mappings
urls = (
    "/blog/(.+)\.html", "blog",
    "/cat/(.+)", "cat",
    "/tag/(.+)", "tag",
    "/admin", admin.admin,
    "/(.*)", "index"
)

### Templates
t_globals = {
    'date' : web.datestr
        }
render = web.template.render('themes/default/', globals=t_globals)

class index:
    def GET(self, path):
        name = path
        return render.index(name)

### main&run
app = web.application(urls, locals())
if __name__ == "__main__":
    app.run()
