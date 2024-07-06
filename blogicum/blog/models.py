from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class PostModel(models.Model):  # Базовая модель поста, чтобы было по DRY

    is_published = models.BooleanField(
        default=True,
        help_text="Снимите галочку, чтобы скрыть публикацию.",
        verbose_name="Опубликовано",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Добавлено"
    )

    class Meta:
        abstract = True


class Category(PostModel):

    title = models.CharField(max_length=256, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(
        unique=True,
        verbose_name="Идентификатор",
        help_text="Идентификатор страницы для URL; "
        "разрешены символы латиницы, цифры, дефис и подчёркивание.",
    )

    class Meta:
        db_table = "category"
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Location(PostModel):

    name = models.CharField(max_length=256, verbose_name="Название места")

    class Meta:
        db_table = "location"
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name


class Post(PostModel):

    title = models.CharField(max_length=256, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата и время публикации",
        help_text="Если установить дату и время в будущем — "
        "можно делать отложенные публикации.",
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
    )
    location = models.ForeignKey(
        to=Location,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        to=Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
    )

    class Meta:
        db_table = "post"
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        default_related_name = 'posts'

    def __str__(self):
        return self.title
