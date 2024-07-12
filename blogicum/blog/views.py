from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import CommentForm, PostForm
from blog.models import Category, Comment, Post, User
from blog.utils import (
    CommentMixin, PostValidMixin, OnlyAuthorMixin, get_available_posts
)


PAGINATION = 10


# Базовые
class IndexView(ListView):
    """Главная страница со лентой всех доступных публикаций"""
    
    template_name = "blog/index.html"
    paginate_by = PAGINATION

    def get_queryset(self):
        return get_available_posts()
    


class CategoryView(ListView):
    """Страница со лентой всех доступных публикаций по категории"""

    template_name = "blog/category.html"
    paginate_by = PAGINATION

    def get_queryset(self):
        return (
            get_available_posts().filter(category__slug=self.kwargs["category_slug"])
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, is_published=True, slug=self.kwargs["category_slug"])
        context["category"] = category
        return context


class PostDetailView(FormMixin, DetailView):
    """Страница детального просмотра выбранной публикации"""

    model = Post
    template_name = "blog/detail.html"
    pk_url_kwarg = "post_id"

    def get_object(self):
        post = super().get_object()
        if post.author == self.request.user:
            return post

        return get_object_or_404(
            get_available_posts(selected_related=False, comment_count=False),
            id=post.id
        )

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            form=CommentForm(),
            comments=self.object.comments.select_related('author')
        )


# Публикации
class PostEditMixin:
    """Конфигурации контроллеров публикаций"""

    model = Post
    form_class = PostForm
    template_name = "blog/create.html"
    pk_url_kwarg = "post_id"


class PostCreateView(LoginRequiredMixin, PostValidMixin, CreateView):
    """Страница создания новой публикации"""

    form_class = PostForm
    template_name = "blog/create.html"

    def get_success_url(self):
        return reverse_lazy(
            "blog:profile", kwargs={"username": self.request.user.username}
        )


class PostUpdateView(
    LoginRequiredMixin, OnlyAuthorMixin,
    PostValidMixin, PostEditMixin, UpdateView
):
    """Страница изменения выбранной публикации"""

    def get_success_url(self):
        return reverse_lazy(
            "blog:post_detail", kwargs={"post_id": self.object.pk}
        )


class PostDeleteView(
    LoginRequiredMixin, OnlyAuthorMixin, PostEditMixin, DeleteView
):
    """Страница удаления выбранной публикации"""

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            form=PostForm(instance=self.object), **kwargs
        )

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', args=[self.request.user.username]
        )


# Комментарии
class CommentCreateView(LoginRequiredMixin, CommentMixin, CreateView):
    """Контроллер создания нового комментария"""

    model = Comment
    form_class = CommentForm
    template_name = 'blog/create.html'
    pk_url_kwarg = "post_id"

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(
            Post,
            id=self.kwargs[self.pk_url_kwarg]
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            form.instance.author = self.request.user
            form.instance.post = self.post_obj
        return super().form_valid(form)


class CommentUpdateView(
    LoginRequiredMixin, OnlyAuthorMixin, CommentMixin, UpdateView
):
    """Контроллер изменения нового комментария"""

    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"
    pk_url_kwarg = "comment_id"


class CommentDeleteView(
    LoginRequiredMixin, OnlyAuthorMixin, CommentMixin, DeleteView
):
    """Контроллер удаления нового комментария"""

    model = Comment
    pk_url_kwarg = "comment_id"
    template_name = "blog/comment.html"


# Профиль
class Profile(ListView):
    """Страница - личный кабинет пользователя со списком ВСЕХ его статей"""

    template_name = 'blog/profile.html'
    paginate_by = PAGINATION

    def get_queryset(self):
        self.author = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        return get_available_posts(
            filter_published=self.request.user != self.author,
            selected_related=False,
            comment_count=True).filter(author=self.author.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        return context


class EditProfile(LoginRequiredMixin, UpdateView):
    """Страница изменения профиля пользователя"""

    model = User
    template_name = 'blog/user.html'
    fields = (
        'username',
        'first_name',
        'last_name',
        'email',
    )

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            "blog:profile",
            kwargs={"username": self.request.user.username}
        )
