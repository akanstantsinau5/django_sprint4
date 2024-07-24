from django.contrib import admin

from .models import Location, Category, Post, Comment

admin.site.empty_value_display = 'Не задано'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'is_published',
        'created_at',
        'name'
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'slug',
    )
    list_editable = (
        'is_published',
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'is_published',
        'title',
        'text',
        'category',
        'pub_date',
    )
    list_editable = (
        'is_published',
        'text',
        'category',
    )
    list_display_links = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'text'
    )
    list_editable = (
        'text',
    )
