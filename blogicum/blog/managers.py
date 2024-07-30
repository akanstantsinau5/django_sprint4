from django.db import models
from django.db.models import Count, Q
from django.utils import timezone


class PostQuerySet(models.QuerySet):

    def published_before_now(self):
        return self.filter(is_published=True, pub_date__lte=timezone.now())

    def published_in_published_category(self):
        return self.published_before_now().filter(category__is_published=True)

    def comment_count(self):
        return self.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    # def accessibility(self, user):
    #     if user.is_authenticated:
    #         user_posts = user.posts.all()
    #         published_posts = user.posts.published_before_now()
    #     return user_posts | published_posts

    def get_related_data(self):
        return self.select_related(
            'author', 'location', 'category'
        ).prefetch_related('comments')
