# ^-^ coding: utf-8 ^-^
"""
Admin operation of Intuition handle all admin operation
@version: $Id$
@author: Libitum<libitum@msn.com>
"""
import urllib
import xml.dom.minidom
import web
import config
import model2

### Url mappings
urls = (
    "/login", "Login",
    "/logout", "Logout",
    "/posts/?(.*)", "Post",
    "/pages/?(.*)", "Page",
    "/links", "Link",
    "/setup", "Setup",
    ".*", "Index"
)
### App initialization
admin = web.application(urls, locals())

### Session initialization
'''
if web.config.get('_session') is None:
    session = web.session.Session(admin, web.session.DiskStore('sessions'))
    web.config._session = session
else:
    session = web.config._session
'''
### Templates initialization
t_globals = {
    'datestr' : web.datestr,
}
render = web.template.render('themes/admin', base="base", globals=t_globals)

### Main handler
class Index:
    def GET(self):
        return render.index()

class Login:
    def GET(self):
        data = web.input()
        if data.has_key("openid.mode"):
            if data.get("openid.mode") == "cancel":
                return "No Access from google!"
            elif data.get("openid.mode") == "id_res":
                params = {
                        "openid.signed" : data.get("openid.signed"),
                        "openid.sig" : data.get("openid.sig"),
                        "openid.mode" : "check_authentication"
                        }
                for key in data.get("openid.signed").split(","):
                    params["openid."+key] = data.get("openid."+key)
                params["openid.ext1.value.firstname"] = data.get("openid.ext1.value.firstname").encode("utf-8")

                URI = self.__discover(data.get("openid.identity"))
                valid = urllib.urlopen(URI, data=urllib.urlencode(params)).read()
                if(valid == "is_valid:true"):
                    if data.get("openid.ext1.value.email") == config.ADMIN:
                        return "Login Successfully!"
                    else:
                        return "Not this user! Please check the ADMIN in config.py"
                else:
                    return "Invalided Authentication!" + valid
            else:
                return "Unknown error"
        else:
            #signin with google through openID
            URI = self.__discover('https://www.google.com/accounts/o8/id')
            
            data = {
                    "openid.mode" : "checkid_setup",
                    "openid.ns" : "http://specs.openid.net/auth/2.0",
                    "openid.return_to" : web.ctx.home + web.ctx.path,
                    "openid.claimed_id" : "http://specs.openid.net/auth/2.0/identifier_select",
                    "openid.identity" : "http://specs.openid.net/auth/2.0/identifier_select",
                    "openid.ns.pape" : "http://specs.openid.net/extensions/pape/1.0",
                    "openid.pape.max_auth_age" : "3600",
                    "openid.ns.ui" : "http://specs.openid.net/extensions/ui/1.0",
                    "openid.ns.ax" : "http://openid.net/srv/ax/1.0",
                    "openid.ax.mode" : "fetch_request",
                    "openid.ax.required" : "email,firstname",
                    "openid.ax.type.email" : "http://schema.openid.net/contact/email",
                    "openid.ax.type.firstname" : "http://axschema.org/namePerson/first"
                }
            raise web.seeother(URI + "?" + urllib.urlencode(data))
    #end of GET

    def __discover(self, url):
        """ Discover authentication URI """
        re = urllib.urlopen(url)
        dom = xml.dom.minidom.parseString(re.read())
        URI = dom.getElementsByTagName('URI')[0].firstChild.data
        return URI
#end of class Login

class Logout:
    '''clear session and return to index of blog'''
    def GET(self):
        pass

class Post:
    '''manage posts'''
    def GET(self, _id):
        return render.post()

class Page:
    '''manage pages'''
    def GET(self, _id):
        return render.post()

class Link:
    '''manage links'''
    def GET(self):
        return render.links()

class Setup:
    '''configuration of blog'''
    def GET(self):
        return render.setup()
