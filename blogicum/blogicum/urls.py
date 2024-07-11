from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import include, path, reverse_lazy

from blogicum import settings

handler404 = "pages.views.error_404"
handler403 = "pages.views.error_403"
handler500 = "pages.views.error_500"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("pages/", include("pages.urls", namespace="pages")),
    path("auth/", include("django.contrib.auth.urls")),
    # В финальном спринте не забыть отрефачить в отдельное приложение users
    path(
        "auth/registration/",
        CreateView.as_view(
            template_name="registration/registration_form.html",
            form_class=UserCreationForm,
            success_url=reverse_lazy("login"),
        ),
        name="registration",
    ),
    path("", include("blog.urls", namespace="blog")),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
    urlpatterns + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
