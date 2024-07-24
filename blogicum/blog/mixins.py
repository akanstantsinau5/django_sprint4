from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect


class CommentAuthorMixin(UserPassesTestMixin):

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={
            'post_pk': self.object.pk
        })

    def test_func(self):
        return self.request.user == self.get_object().author


class EditPostMixin(UserPassesTestMixin):

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={
            'post_pk': self.object.pk
        })

    def test_func(self):
        return self.request.user == self.get_object().author

    def handle_no_permission(self):
        post_pk = self.kwargs['post_pk']
        return HttpResponseRedirect(reverse(
            'blog:post_detail', kwargs={'post_pk': post_pk}
        ))
