from django.shortcuts import get_list_or_404, get_object_or_404, render

from blog.models import Category
from blog.utils import get_available_posts


def index(request):

    post_list = (get_available_posts().order_by('-pub_date')[:5])

    context = {
        "post_list": post_list
    }

    return render(request, "blog/index.html", context)


def post_detail(request, post_id):

    post = get_object_or_404(get_available_posts(), pk=post_id)

    context = {
        "post": post,
    }

    return render(request, "blog/detail.html", context)


def category_posts(request, category_slug):

    category = get_object_or_404(
        Category.objects.filter(
            slug=category_slug,
            is_published=True)
    )

    post_list = get_list_or_404(
        get_available_posts()
        .filter(category=category)
    )

    context = {
        "post_list": post_list,
        "category": category
    }

    return render(request, "blog/category.html", context)
