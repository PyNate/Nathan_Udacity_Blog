import re
from handlers import Handler
from users import User

_name = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
_pw = re.compile(r"^.{3,20}$")
_email = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


def _valid_username(s):
    return _name.match(s)


def _valid_pw(s):
    return _pw.match(s)


def _valid_email(s):
    return _email.match(s)


class SignupPage(Handler):

    def render_signup(self):
        self.render('signup.html',
                    usererror='',
                    passerror='',
                    verifyerror='',
                    emailerror='',
                    username='',
                    email='')

    def get(self):
        if self.get_secure_cookie('user_id'):
            self.redirect('/blog/welcome')
        else:
            self.render_signup()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        founderror = False
        usererror = ''
        passerror = ''
        verifyerror = ''
        emailerror = ''
        if self.get_secure_cookie('user_id'):
            self.redirect('/blog/welcome')
        else:
            if not (username and _valid_username(username)):
                usererror = 'Please enter a valid username.'
                founderror = True
            if not (password and _valid_pw(password)):
                passerror = 'Please enter a valid password.'
                founderror = True
            if not (password == verify):
                verifyerror = 'Your passwords did not match. Please try again.'
                founderror = True
            if email and not _valid_email(email):
                emailerror = 'Please enter a valid email address.'
                founderror = True
            if founderror:
                self.render('signup.html',
                            usererror=usererror,
                            passerror=passerror,
                            verifyerror=verifyerror,
                            emailerror=emailerror,
                            username=username,
                            email=email)
            else:
                user = User.by_name(username)
                if user:
                    usererror = 'That username is already in use.'
                    self.render('signup.html', usererror=usererror)
                else:
                    new_user = User.register(username, password, email)
                    new_user.put()
                    self.set_login(new_user)
                    self.redirect('/blog/welcome')


class WelcomePage(Handler):

    def get(self):
        user_id = self.get_secure_cookie('user_id')
        if user_id:
            user = User.by_id(int(user_id))
            username = user.username
            self.render('welcome.html', username=username)
        else:
            self.redirect('/blog/signup')


class LoginPage(Handler):

    def get(self):
        if self.get_secure_cookie('user_id'):
            self.redirect('/blog/welcome')
        else:
            self.render('login.html', username='', error='')

    def render_error(self, **kw):
        self.render('login.html', error='Invalid username or password.', **kw)

    def post(self):
        if self.get_secure_cookie('user_id'):
            self.redirect('/blog/welcome')
        else:
            username = self.request.get('username')
            password = self.request.get('password')
            user = User.login(username, password)
            if not (username and password and user):
                self.render_error(username=username)
            else:
                self.set_login(user)
                self.redirect('/blog/welcome')


class Logout(Handler):

    def get(self):
        self.response.delete_cookie('user_id')
        self.redirect('/blog/signup')