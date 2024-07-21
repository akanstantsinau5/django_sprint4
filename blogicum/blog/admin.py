from django.contrib import admin

from .models import Location, Category, Post

admin.site.empty_value_display = 'Не задано'


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'is_published',
        'created_at',
        'name'
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'slug',
    )
    list_editable = (
        'is_published',
    )


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


admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
