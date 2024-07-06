﻿from django.utils import timezone

from blog.models import Post


def get_available_posts():
    """Получение постов из БД"""
    return (Post.objects
            .select_related("category", "location", "author")
            .filter(is_published=True,
                    category__is_published=True,
                    pub_date__lte=timezone.now())
            )