from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from .managers import PostQuerySet

User = get_user_model()


class PublishedModel(models.Model):
    title = models.CharField('Заголовок', max_length=256)
    is_published = models.BooleanField(
        'Опубликовано', default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True


class Location(PublishedModel):
    title = None
    name = models.CharField('Название места', max_length=256)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Category(PublishedModel):
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор', max_length=64, unique=True,
        help_text='Идентификатор страницы для URL; разрешены символы латиницы,'
        ' цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Post(PublishedModel):
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации', default=timezone.now,
        help_text='Если установить дату и время в будущем — '
        'можно делать отложенные публикации.'
    )
    image = models.ImageField('Фото', upload_to='post_images', blank=True)
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
    )
    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
    )
    objects = PostQuerySet.as_manager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)
        default_related_name = 'posts'

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} at {self.created_at}'
