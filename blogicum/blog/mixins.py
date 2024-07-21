from django.utils import timezone
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from .forms import CommentForm
from .models import Post, Category, Comment

# Marking Mixin Categories for better readibility:
# Categories: Published, Profile, Post, Comment


User = get_user_model()


# Published
class PublishedMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_published=True, pub_date__lte=timezone.now())


class PublisheInCategorydMixin(PublishedMixin):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(category__is_published=True)


# Comment
class CommentCountMixin:
    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            comment_count=Count('comment')
        )
        return queryset


class CommentAuthorMixin(UserPassesTestMixin):
    def get_object(self):
        return get_object_or_404(Comment, pk=self.kwargs['comment_pk'])

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


# Post
class PostDetailMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset.filter(
                is_published=True
            ) | queryset.filter(author=self.request.user)
        else:
            return queryset.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comment.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', pk=self.object.pk)
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class PostAuthorMixin(UserPassesTestMixin):
    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class EditPostMixin(UserPassesTestMixin):
    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        post_pk = self.kwargs['pk']
        return redirect('blog:post_detail', pk=post_pk)


class CategoryPostMixin:
    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        queryset = super().get_queryset().filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


# Profile
class UserProfileMixin:
    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        return super().get_queryset().filter(
            author=self.user
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.user
        return context
