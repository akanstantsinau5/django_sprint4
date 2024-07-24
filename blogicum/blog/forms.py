from django import forms

from .models import Post, Comment, User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
