from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse


class BaseMixin(UserPassesTestMixin):

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs['post_pk']])

    def test_func(self):
        return self.request.user == self.get_object().author


class CommentAuthorMixin(BaseMixin):
    pass


class EditPostMixin(BaseMixin):

    def handle_no_permission(self):
        return redirect('blog:post_detail', self.kwargs['post_pk'])
