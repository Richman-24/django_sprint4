from http import HTTPStatus

from django.shortcuts import render
from django.views.generic import TemplateView


class AboutPage(TemplateView):
    template_name = "pages/about.html"


class RulesPage(TemplateView):
    template_name = "pages/rules.html"


def error_404(request, exception):
    return render(request, "pages/404.html", status=HTTPStatus.NOT_FOUND)


def error_403(request, reason=""):
    return render(request, "pages/403csrf.html", status=HTTPStatus.FORBIDDEN)


def error_500(request):
    return render(
        request,
        "pages/500.html",
        status=HTTPStatus.INTERNAL_SERVER_ERROR
    )
