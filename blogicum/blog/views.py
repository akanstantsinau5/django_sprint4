from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView, DetailView, UpdateView, CreateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .mixins import CommentAuthorMixin, EditPostMixin
from .forms import CommentForm, PostForm, ProfileForm
from .models import Post, Category, Comment, User


POSTS_ON_PAGE = 10


class PostListView(ListView):
    model = Post
    ordering = '-pub_date'
    template_name = 'blog/index.html'
    paginate_by = POSTS_ON_PAGE

    def get_queryset(self):
        return super().get_queryset().published_in_published_category(
        ).comment_count()


class DetailPostView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_pk'

    def get_object(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        if not post.author == self.request.user:
            return get_object_or_404(
                Post.objects.published_in_published_category(),
                pk=self.kwargs.get('post_pk')
            )
        return post

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            form=CommentForm(),
            comments=self.object.comments.order_by('created_at'),
            **kwargs,
        )

    def test_func(self):
        return self.get_object().author == self.request.user


class CategoryPostView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = POSTS_ON_PAGE

    def get_category(self):
        return get_object_or_404(Category, slug=self.kwargs.get(
            'category_slug'), is_published=True)

    def get_queryset(self):
        return self.get_category().posts.published_in_published_category(
        ).comment_count()

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            category=self.get_category(),
            **kwargs,
        )


class ProfileView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = POSTS_ON_PAGE

    def get_author(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        author = self.get_author()
        if not author == self.request.user:
            return author.posts.comment_count(
            ).published_in_published_category()
        return author.posts.comment_count()

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            profile=self.get_author(),
            **kwargs,
        )


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'

    def get_success_url(self):
        return reverse(
            'blog:profile', args=[self.request.user.username]
        )

    def get_object(self):
        return self.request.user


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile', args=[self.request.user.username]
        )


class PostView(LoginRequiredMixin):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_pk'


class EditPostView(PostView, EditPostMixin, UpdateView):
    form_class = PostForm


class DeletePostView(PostView, UserPassesTestMixin, DeleteView):
    success_url = reverse_lazy('blog:index')

    def test_func(self):
        return self.request.user == self.get_object().author


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={
            'post_pk': self.kwargs['post_pk']
        })


class CommentView(LoginRequiredMixin, CommentAuthorMixin):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_pk'


class EditCommentView(CommentView, UpdateView):
    form_class = CommentForm


class DeleteCommentView(CommentView, DeleteView):
    pass
