from django.core.management.base import BaseCommand, CommandError
from core.User.factories import UserFactory
from core.Category.factories import CategoryFactory
from core.Post.factories import PostFactory
from core.Comment.factories import CommentFactory
from core.Likes.factories import PostLikeFactory, CommentLikeFactory
from core.User.models import User
from core.Category.models import Category
from core.Post.models import Post
from core.Comment.models import Comment


class Command(BaseCommand):
    USERS_COUNTER = 15
    CATEGORY_COUNTER = 10
    POST_PER_USER_COUNTER = 15
    COMMENTS_COUNTER = 10
    EACH_POST_LIKED_COUNTER = 5
    EACH_COMMENT_LIKED = 5

    def add_arguments(self, parser):
        parser.add_argument("-c", "--clean",
                            dest="clean_db",
                            type=bool,
                            default=None)
        parser.add_argument("-uc", "--user-counter",
                            dest="user_counter",
                            type=int,
                            default=None)
        parser.add_argument("-cc", "--category-counter",
                            dest="category_counter",
                            type=int,
                            default=None)
        parser.add_argument("-pc", "--post-counter",
                            dest="post_counter",
                            type=int,
                            default=None)
        parser.add_argument("-mc", "--comments-counter",
                            dest="comments_counter",
                            type=int,
                            default=None)
        parser.add_argument("-plc", "--post-like-counter",
                            dest="post_like_counter",
                            type=int,
                            default=None)
        parser.add_argument("-clc", "--comment-like-counter",
                            dest="comment_like_counter",
                            type=int,
                            default=None)

    def handle(self, *args, **options):
        clean_db = options.get('clean_db', False)
        user_counter = options.get('user_counter', self.USERS_COUNTER)
        category_counter = options.get('category_counter', self.CATEGORY_COUNTER)
        post_counter = options.get('post_counter', self.POST_PER_USER_COUNTER)
        comments_counter = options.get('comments_counter', self.COMMENTS_COUNTER)
        post_like_counter = options.get('post_like_counter', self.EACH_POST_LIKED_COUNTER)
        comment_like_counter = options.get('comment_like_counter', self.EACH_COMMENT_LIKED)

        if clean_db:
            Post.objects.all().delete()
            Category.objects.all().delete()
            User.objects.filter(is_staff=False, is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('DB cleaned'))

        for _ in range(category_counter):
            category = CategoryFactory.create()
            category.save()
        self.stdout.write(self.style.SUCCESS('Created %s Category instances') % self.CATEGORY_COUNTER)

        for k in range(user_counter):
            user = UserFactory.create()
            user.save()

            for category in Category.objects.all():
                for i in range(post_counter):
                    post = PostFactory.create(category=category, author=user)
                    post.save()

                    if post_like_counter and i % post_like_counter == 0:
                        like = PostLikeFactory.create(post=post, user=user)
                        like.save()

                    for j in range(comments_counter):
                        comment = CommentFactory.create(post=post, author=user)
                        comment.save()

                        if comment_like_counter and j % comment_like_counter == 0:
                            like = CommentLikeFactory.create(comment=comment, user=user)
                            like.save()

                    if i and i % 100 == 0:
                        self.stdout.write(
                            self.style.SUCCESS('%s Posts created with %s comments') % (i, comments_counter))

            self.stdout.write(self.style.SUCCESS('%s Users completed') % str(k + 1))

        info_string = f'\n\tCategories: {Category.objects.count()}\n\tUsers: {User.objects.count()}\n\tPosts: {Post.objects.count()}\n\tComments: {Comment.objects.count()}\n\t'  # noqa
        self.stdout.write(self.style.SUCCESS('Successfully filled in DB %s') % info_string)
