import os
import webapp2
import jinja2

from google.appengine.ext import db 

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)


class MainHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t=jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class BlogPosts2(db.Model):
    title = db.StringProperty(required = True)
    post = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True) #auto timestamp submissions

class Index(webapp2.RequestHandler):
    """Handles requests coming into '/'  """
    def get(self):
        self.redirect('/blog') #auto redirect
    #t = jinja_env.get_template("index.html") #option to display link
    #self.render(t)

class Blog(MainHandler):
    def render_blogs(self, title="", post=""):
        posts = db.GqlQuery("SELECT * FROM BlogPosts2 ORDER BY created DESC LIMIT 5")
        self.render("blog.html", title = title, post = post, posts = posts)

    def get(self):
        self.render_blogs()

class NewPost(MainHandler):
    def render_form(self, title="", post="", error = ""):
        self.render("newpost.html", title = title, post = post, error = error)
    
    def get(self):
        self.render_form()

    def post(self): 
        title = self.request.get("title")
        post = self.request.get("post")

        if title and post: 
            p = BlogPosts2(title = title, post = post)
            p.put()
            self.redirect('/blog/' + str(p.key().id()))

        else: 
            error="Whoops! Please fill out both fields."
            self.render_form(title, post, error)

class ViewPostHandler(MainHandler):
    def get(self, id):
        #self.response.write(id)
        if id: 
            single_post = BlogPosts2.get_by_id(int(id))
            self.render("permalink.html", title = single_post.title, post = single_post.post)
        else:
            self.redirect('/blog')


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/blog', Blog),
    ('/newpost', NewPost),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)

