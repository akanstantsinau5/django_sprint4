from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView, DetailView, UpdateView, CreateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .mixins import (CommentAuthorMixin, EditPostMixin)
from .forms import PostForm, CommentForm, ProfileForm
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

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if not post.is_published and post.author != self.request.user:
            raise Http404()
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all().order_by('created_at')
        return context


class CategoryPostView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = POSTS_ON_PAGE

    def get_queryset(self):
        request_slug = self.kwargs.get('category_slug')
        request_category = get_object_or_404(Category, slug=request_slug)

        if not request_category.is_published:
            raise Http404()

        return Post.objects.filter(
            category=request_category
        ).published_before_now().comment_count().order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category, slug=self.kwargs.get('category_slug')
        )
        return context


class ProfileView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = POSTS_ON_PAGE

    def get_queryset(self):
        request_username = self.kwargs.get('username')
        request_author = get_object_or_404(User, username=request_username)
        return Post.objects.filter(
            author=request_author
        ).comment_count().order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_username = self.kwargs.get('username')
        context['profile'] = get_object_or_404(User, username=request_username)
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={
            'username': self.request.user.username
        })

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


class EditPostView(LoginRequiredMixin, EditPostMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_pk'


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_pk'
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
            'post_pk': self.object.post.pk
        })


class EditCommentView(LoginRequiredMixin, CommentAuthorMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_pk'


class DeleteCommentView(LoginRequiredMixin, CommentAuthorMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_pk'
