from handlers import Handler
from google.appengine.ext import db


def get_entries():
    return db.GqlQuery("SELECT * FROM Blog ORDER BY time DESC")


class BlogPage(Handler):
    def get(self):
        entries=get_entries()
        self.render("blog.html", entries=entries)