﻿from django.urls import path

from blog import views


app_name = "blog"

urlpatterns = [
    path(  # Статьи по категории
        "category/<slug:category_slug>/",
        views.CategoryView.as_view(),
        name="category_posts",
    ),
    path(  # Создать статью
        "posts/create/",
        views.PostCreateView.as_view(),
        name="create_post",
    ),
    path(  # Изменить статью
        "posts/<int:post_id>/edit/",
        views.PostUpdateView.as_view(),
        name="edit_post",
    ),
    path(  # Удалить статью
        "posts/<int:post_id>/delete/",
        views.PostDeleteView.as_view(),
        name="delete_post",
    ),
    path(  # Изменить коммент
        "posts/<int:post_id>/edit_comment/<int:comment_id>/",
        views.CommentUpdateView.as_view(),
        name="edit_comment",
    ),
    path(  # Удалить коммент
        "posts/<int:post_id>/delete_comment/<int:comment_id>/",
        views.CommentDeleteView.as_view(),
        name="delete_comment",
    ),
    path(  # Создать коммент
        "posts/<int:post_id>/comment/",
        views.CommentCreateView.as_view(),
        name="add_comment",
    ),
    path(  # Читать полностью \ Показать статью
        "posts/<int:post_id>/",
        views.PostDetailView.as_view(),
        name="post_detail",
    ),
    path(  # Изменить профиль
        "edit_profile/",
        views.EditProfile.as_view(),
        name="edit_profile",
    ),
    path(  # Просмотреть профиль
        "profile/<slug:username>/", views.Profile.as_view(), name="profile"
    ),
    path(  # Главная
        "", views.IndexView.as_view(), name="index"
    ),
]
