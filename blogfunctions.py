from handlers import Handler
from google.appengine.ext import db
from blog import Blog


def get_entries():
    entries = db.GqlQuery("SELECT * FROM Blog ORDER BY time DESC")
    return entries


class BlogPage(Handler):
    def get(self):
        entries = get_entries()
        self.render("blog.html", entries=entries)


class NewPost(Handler):
    def get(self):
        self.render("newpost.html", user_title="", user_content="", error="")

    def post(self):
        user_title = self.request.get('subject')
        user_content = self.request.get('content')
        if not (user_title and user_content):
            self.render("newpost.html",
                        user_title=user_title,
                        user_content=user_content,
                        error="Please enter both a title and content.")
        else:
            post = Blog(title=user_title, entry=user_content)
            key = post.put()
            self.redirect("/blog/%d" % key.id())


class PostPage(Handler):
    def get(self, post_id):
        post = Blog.get_by_id(int(post_id))
        self.render("blog.html", entries=[post])