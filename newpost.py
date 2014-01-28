from handlers import Handler
from blog import Blog


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
