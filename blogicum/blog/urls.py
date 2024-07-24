from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path(
        'profile/<str:username>/',
        views.ProfileView.as_view(),
        name='profile'),
    path(
        'edit_profile/',
        views.EditProfileView.as_view(),
        name='edit_profile'),
    path(
        'posts/<int:post_pk>/',
        views.DetailPostView.as_view(),
        name='post_detail'),
    path(
        'posts/<int:post_pk>/comment/',
        views.AddCommentView.as_view(),
        name='add_comment'),
    path(
        'posts/<int:post_pk>/edit/',
        views.EditPostView.as_view(),
        name='edit_post'),
    path(
        'posts/<int:post_pk>/edit_comment/<int:comment_pk>',
        views.EditCommentView.as_view(),
        name='edit_comment'),
    path('posts/create/', views.CreatePostView.as_view(), name='create_post'),
    path(
        'posts/<int:post_pk>/delete/',
        views.DeletePostView.as_view(),
        name='delete_post'),
    path(
        'posts/<int:post_pk>/delete_comment/<int:comment_pk>/',
        views.DeleteCommentView.as_view(),
        name='delete_comment'),
    path('category/<slug:category_slug>/', views.CategoryPostView.as_view(),
         name='category_posts'),
]
