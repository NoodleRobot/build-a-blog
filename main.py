import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir=os.path.join(os.path.dirname(__file__), 'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                autoescape = True)
                                

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class BlogPost(db.Model):
    title = db.StringProperty (required = True)
    blog = db.TextProperty(required = True) #TextProperty class for long strings
    datestamp = db.DateProperty(auto_now_add = True) #auto datestamp submissions

class MainPage(Handler):
    def render_front(self, title="", blog="", error=""): #keeps these vales empty until something passed in, i think?
        blogs = db.GqlQuery("SELECT * FROM BlogPost "
                            "ORDER BY creted DESC ")

        self.render("main-blog.html", title = title, blog = blog, error = error, blogs = blogs)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        blog = self.request.get("blog")

        if title and blog:
            b = Blog(title = title, blog = blog)#get blog object in success case
            b.put() #stores new art object in database

            self.redirect("/")#redirect back to empty form
        else:
            error="DOES NOT COMPUTE!!"
            self.render_front(title, blog, error)#sends in error, title and blog


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
