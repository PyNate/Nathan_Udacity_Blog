from handlers import Handler
import webapp2
from userfunctions import SignupPage, WelcomePage, LoginPage, Logout
from blogpage import BlogPage
from postpage import PostPage
from newpost import NewPost


class MainPage(Handler):
    def get(self):
        self.render("front.html")


application = webapp2.WSGIApplication([('/', MainPage),
                                       ('/blog', BlogPage),
                                       ('/blog/newpost', NewPost),
                                       ('/blog/(\d+)', PostPage),
                                       ('/blog/signup', SignupPage),
                                       ('/blog/welcome', WelcomePage),
                                       ('/blog/login', LoginPage),
                                       ('/blog/logout', Logout)],
                                      debug=True)