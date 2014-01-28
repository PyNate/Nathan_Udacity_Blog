from blog import Blog
from handlers import Handler


class PostPage(Handler):
    def get(self, post_id):
        post = Blog.get_by_id(int(post_id))
        self.render("blog.html", entries=[post])
