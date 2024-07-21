from django.db.models.base import Model as Model
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.views.generic import (
    ListView, DetailView, UpdateView, CreateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import (
    PublisheInCategorydMixin, CommentCountMixin, UserProfileMixin,
    CommentAuthorMixin, PostAuthorMixin, EditPostMixin, PostDetailMixin,
    CategoryPostMixin)
from .forms import PostForm, CommentForm, ProfileForm
from .models import Post, Comment


User = get_user_model()


posts_on_page = 10


class PostListView(PublisheInCategorydMixin, CommentCountMixin, ListView):
    model = Post
    ordering = '-pub_date'
    template_name = 'blog/index.html'
    paginate_by = posts_on_page


class PostDetailView(PostDetailMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'


class CategoryPostView(PublisheInCategorydMixin, CategoryPostMixin, ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'paje_obj'
    paginate_by = posts_on_page


class ProfileView(UserProfileMixin, CommentCountMixin, ListView):
    model = Post
    template_name = 'blog/profile.html'
    context_object_name = 'paje_obj'
    paginate_by = posts_on_page


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'
    content_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def form_valid(self, form):
        self.object = form.save()
        return redirect('blog:profile', username=self.object.username)


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class EditPostView(LoginRequiredMixin, EditPostMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})


class EditCommentView(LoginRequiredMixin, CommentAuthorMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.get_object()
        return context


class PostDeleteView(LoginRequiredMixin, PostAuthorMixin, DeleteView):
    model = Post,
    template_name = 'blog/detail.html'
    success_url = reverse_lazy('blog:index')


class CommentDeleteView(LoginRequiredMixin, CommentAuthorMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
