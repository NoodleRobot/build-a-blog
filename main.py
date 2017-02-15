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

class BlogPosts(db.Model): #represent submission from user, inherits from db.model (creates entity)
    title = db.StringProperty(required = True)#tells google this is string type
    blog = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)#auto date+time stamps submissions
                                                    #when adding to db

class Index(Handler):
    """Handles  requests coming into '/'  """
    def get(self):
        self.redirect('/blog') #auto redirect
        #t = jinja_env.get_template("index.html") #option to display link
        #self.render(t)

class Blog(Handler):
    def render_blogs(self, title="", blog=""):
        blogs = db.GqlQuery("SELECT * FROM BlogPosts "
                            "ORDER BY created DESC "
                            "LIMIT 5; ")

        self.render("blog.html", title = title, blog = blog, blogs = blogs)

    def get(self):
        self.render_blogs()

class NewPost(Handler):
    def render_form(self, title="", blog="", error=""):
        self.render("newpost.html", title = title, blog = blog, error = error)

    def get(self):
        self.render_form()

    def post(self):
        title = self.request.get("title")
        blog = self.request.get("blog")

        if title and blog:
            b = BlogPosts(title = title, blog = blog) #gets blog object in success case
            b.put() #stores new blog object in database
            self.redirect("/blog/" + str(b.key().id())) #send user to permalink in success case

        else:
            error="OH NO, DOES NOT COMPUTE!! Please fill out both fields."
            self.render_form(title, blog, error) #renders form again
                                                #w/ error message

class ViewPostHandler(Handler):  

    def get(self, id):
        #single_post = BlogPosts.get_by_id(int(id))
        #self.response.write(id)
        #self.response.write(single_post)
        #t = jinja_env.get_template('permalink.html')
        #content = t.render(title = title, blog = blog) #'title' not defined...
        #content = t.render(post_title = single_post.title, post = single_post.blog)
        #self.response.write(content)

        if id:
            single_post = BlogPosts.get_by_id(int(id))
            #self.response.write(type(single_post)
            #self.render("permalink.html", title=title, blog=blog)
            #self.render("permalink.html", title=single_post.title, blog=single_post.blog)
            t=jinja_env.get_template("permalink.html")
            content=t.render(title=title, blog=blog)
            self.response.out.write(content)
        else:
            self.redirect('/blog')    

        




app = webapp2.WSGIApplication([
    ('/', Index),
    ('/blog', Blog),
    ('/newpost', NewPost),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
