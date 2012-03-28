#!/usr/bin/env python
# ^-^ coding: utf-8 ^-^
"""
The main entrance of Intuition, mapping urls to different Controlor
@version: $Id$
@author: Libitum<libitum@msn.com>
"""
import os, sys
import web

abspath = os.path.dirname(__file__)
sys.path.append(abspath)
import admin
import blog

### Url mappings
urls = (
    "/admin", admin.admin,
    "", blog.blog
)

### main&run
app = web.application(urls, locals())
if __name__ == "__main__":
    app.run()
else:
    application = app.wsgifunc()
