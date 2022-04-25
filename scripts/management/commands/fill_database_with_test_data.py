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
    CLEAN_UP_DB = True

    USERS_COUNTER = 15
    CATEGORY_COUNTER = 10
    POST_PER_USER_COUNTER = 15
    COMMENTS_COUNTER = 10
    EACH_POST_LIKED_COUNTER = 5
    EACH_COMMENT_LIKED = 5

    def clear_db(self):
        Post.objects.all().delete()
        Category.objects.all().delete()
        User.objects.filter(is_staff=False, is_superuser=False).delete()

    def handle(self, *args, **options):
        if self.CLEAN_UP_DB:
            self.clear_db()
            self.stdout.write(self.style.SUCCESS('DB cleaned'))

        for _ in range(self.CATEGORY_COUNTER):
            category = CategoryFactory.create()
            category.save()
        self.stdout.write(self.style.SUCCESS('Created %s Category instances') % self.CATEGORY_COUNTER)

        for k in range(self.USERS_COUNTER):
            user = UserFactory.create()
            user.save()

            for category in Category.objects.all():
                for i in range(self.POST_PER_USER_COUNTER):
                    post = PostFactory.create(category=category, author=user)
                    post.save()

                    if i % self.EACH_POST_LIKED_COUNTER == 0:
                        like = PostLikeFactory.create(post=post, user=user)
                        like.save()

                    for j in range(self.COMMENTS_COUNTER):
                        comment = CommentFactory.create(post=post, author=user)
                        comment.save()

                        if j % self.EACH_COMMENT_LIKED == 0:
                            like = CommentLikeFactory.create(comment=comment, user=user)
                            like.save()

                    if i and i % 100 == 0:
                        self.stdout.write(
                            self.style.SUCCESS('%s Posts created with %s comments') % (i, self.COMMENTS_COUNTER))

            self.stdout.write(self.style.SUCCESS('%s Users completed') % k)

        info_string = f'\n\tCategories: {Category.objects.count()}\n\tUsers: {User.objects.count()}\n\tPosts: {Post.objects.count()}\n\tComments: {Comment.objects.count()}\n\t' # noqa
        self.stdout.write(self.style.SUCCESS('Successfully filled in DB %s') % info_string)
