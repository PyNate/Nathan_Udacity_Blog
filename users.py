from google.appengine.ext import db
import random
import string
import hashlib


def _make_salt(length = 5):
    """Creates a random string of letters for use in hashing passwords"""
    return ''.join(random.choice(string.letters) for x in xrange(length))


def _make_pw_hash(name, pw, salt=None):
    """Creates a hashed version of the password to store in the database"""
    if not salt:
        salt = _make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == _make_pw_hash(name, password, salt)


class User(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)  #This will be a hashed version of the passwword.
    email = db.StringProperty()

    @classmethod
    def by_id(cls, user_id):
        """Returns the User object from the database that matches the user_id"""
        return User.get_by_id(user_id)

    @classmethod
    def by_name(cls, username):
        """Returns the User object from the database that matches the username"""
        return User.all().filter('username =', username).get()

    @classmethod
    def register(cls, username, pw, email=None):
        """Used to create a new User object ready to be added to the database"""
        pw_hash = _make_pw_hash(username, pw)
        return User(username=username, password=pw_hash, email=email)

    @classmethod
    def login(cls, username, pw):
        """Returns a user object if the username and password are valid"""
        user = cls.by_name(username)
        if user and valid_pw(username, pw, user.password):
            return user

