# ^-^ coding: utf-8 ^-^
"""
Handle all operation from blog.
@version: $Id$
@author: Libitum<libitum@msn.com>
"""
import web

### Url mappings
urls = (
    "/blog/(.+)\.html", "Article",
    "/cat/(.+)", "Category",
    "/tag/(.+)", "Tag",
    "/(.+)", "Article",
    "/", "Articles"
)

### App initialization
blog = web.application(urls, locals())

### Templates initialization
t_globals = {
}
render = web.template.render('themes/imbalance', base="base", globals=t_globals)

### Main handler
class Articles:
    def GET(self):
        return render.articles()
