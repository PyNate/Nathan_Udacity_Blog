import webapp2
import jinja2
import os
from google.appengine.ext import db
import hmac
from secret import SECRET


def _hash_str(s):
    """Creates a hashed string using a secret key"""
    return hmac.new(SECRET, s).hexdigest()

def _make_secure_val(s):
    """Creates a string containing the input followed by '|' and the hashed input"""
    return "%s|%s" % (s, _hash_str(s))

def _check_secure_val(h):
    val = h.split('|')[0]
    if h == _make_secure_val(val):
        return val


base_dir = os.path.dirname(__file__)
template_dir = os.path.join(base_dir, 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, cookie, val):
        """Creates and sets a hashed cookie"""
        sec_val=_make_secure_val(val)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (cookie, sec_val))

    def get_secure_cookie(self, cookie):
        """Returns requested cookie if the cookie is valid"""
        sec_val = self.request.cookies.get(cookie)
        return sec_val and _check_secure_val(sec_val)

    def set_login(self, user):
        """Sets a user cookie"""
        self.set_secure_cookie('user_id', str(user.key().id()))

    def remove_cookie(self, cookie):
        self.response.headers.add_header('Set-Cookie', '%s=; Path=/' % cookie)
