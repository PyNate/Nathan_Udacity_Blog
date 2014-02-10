from handlers import Handler
import webapp2
from userfunctions import SignupPage, WelcomePage, LoginPage, Logout
from blogfunctions import BlogPage, PostPage, NewPost


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