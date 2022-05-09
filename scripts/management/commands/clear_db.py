from django.core.management.base import BaseCommand
from core.User.models import User
from core.Category.models import Category
from core.Post.models import Post


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("-s", "--staff",
                            dest="is_staff",
                            type=bool,
                            default=False)
        parser.add_argument("-u", "--superuser",
                            dest="is_superuser",
                            type=bool,
                            default=False)

    def handle(self, *args, **options):
        is_staff = options.get('is_staff', False)
        is_superuser = options.get('is_superuser', False)
        user_filter = {
            'is_staff': is_staff,
            'is_superuser': is_superuser,
        }

        Post.objects.all().delete()
        Category.objects.all().delete()
        User.objects.filter(**user_filter).delete()

        self.stdout.write(self.style.SUCCESS('DB cleaned Posts and Categories with related objects'))
        self.stdout.write(self.style.SUCCESS('DB cleaned Users with filter %s' % user_filter))
