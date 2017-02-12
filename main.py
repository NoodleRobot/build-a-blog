import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir=os.path.join(os.path.dirname(__file__), 'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                autoescape = True) #autoescape will escape html

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t=jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        self.write(self.render_str(template, **kw))

class Blog(db.Model): #represent submission from user, inherits from db.model (creates entity)
    title = db.StringProperty(required = True)#tells google this is string type
    blog = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)#date stamps submission-look in docs for more

    
class MainPage(Handler):
    def render_front(self, title="", blog="", error=""):
        blogs = db.GqlQuery("SELECT * FROM Blog "
                            "ORDER BY created DESC ") #stores query

        self.render("blog.html", title=title, blog=blog, error=error, blogs=blogs) #pass in variables so 
                                                                #they can be used in the form

    def get (self):
        self.render_front()

    def post(self):
        title=self.request.get("title")
        blog=self.request.get("blog")

        if title and blog:
            b = Blog(title=title, blog=blog)#get blog object in success case
            b.put() #stores new blog object in database

            self.redirect("/")#redirect back to empty form
        else:
            error="DOES NOT COMPUTE!!"
            self.render_front(title, blog, error)#sends in error, title and blog




app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
