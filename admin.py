# ^-^ coding: utf-8 ^-^
"""
Admin operation of Plod.py. handle all admin operation
@version: $Id$
@author: Libitum<libitum@msn.com>
"""
import urllib
import xml.dom.minidom
import web

### Url mappings
urls = (
    "/login", "Login",
    "/(.*)", "Index"
)

class Index:
    def GET(self, path):
        return "hello " + path + " in admin"

class Login:
    def GET(self):
        if web.input().has_key("openid.mode"):
            data = web.input()
            if data.get("openid.mode") == "cancel":
                return "No Access from google!"
            elif data.get("openid.mode") == "id_res":
                #TODO login success
                return "Login success"
            else:
                return "Unknown error"
        else:
            #signin with google through openID
            re = urllib.urlopen('https://www.google.com/accounts/o8/id')
            dom = xml.dom.minidom.parseString(re.read())
            URI = dom.getElementsByTagName('URI')[0].firstChild.data
            
            data = {
                    "openid.mode" : "checkid_setup",
                    "openid.ns" : "http://specs.openid.net/auth/2.0",
                    "openid.return_to" : web.ctx.home,
                    "openid.claimed_id" : "http://specs.openid.net/auth/2.0/identifier_select",
                    "openid.identity" : "http://specs.openid.net/auth/2.0/identifier_select",
                    "openid.ns.ui" : "http://specs.openid.net/extensions/ui/1.0",
                    "openid.ns.ax" : "http://openid.net/srv/ax/1.0",
                    "openid.ax.mode" : "fetch_request",
                    "openid.ax.required" : "email",
                    "openid.ax.type.email" : "http://schema.openid.net/contact/email"
                }
            raise web.seeother(URI + "?" + urllib.urlencode(data))

admin = web.application(urls, locals())
