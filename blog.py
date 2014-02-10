from google.appengine.ext import db


class Blog(db.Model):
    title = db.StringProperty(required=True)
    entry = db.TextProperty(required=True)
    time = db.DateTimeProperty(auto_now_add=True)



