from core.utils.string import is_empty
from post.models import Post


class PostService:

    @staticmethod
    def create(
            title,
            content,
            author,
    ):
        post = Post()
        post.title = title
        post.content = content
        post.author = author
        post.save()
        return post

    @staticmethod
    def filter(
            qs=None,
            pk=None,
            author_id=None
    ):
        if qs is None:
            qs = Post.objects.all()

        if not is_empty(pk):
            qs = qs.filter(id=pk)

        if not is_empty(author_id):
            qs = qs.filter(author_id=author_id)

        return qs
