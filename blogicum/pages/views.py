from django.shortcuts import render


def error_404(request, exception):
    return render(request, "pages/404.html", status=404)

def error_403(request, reason=""):
    return render(request, "pages/403_csrf.html", status=403)

def error_500(request):
    return render(request, "pages/500.html", status=500)

def about(request):
    return render(request, "pages/about.html")


def rules(request):
    return render(request, "pages/rules.html")
