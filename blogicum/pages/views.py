from django.views.generic import TemplateView
from django.shortcuts import render


class AboutView(TemplateView):
    template_nam = 'pages/about.html'


class RulesView(TemplateView):
    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason='', exception=None):
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    return render(request, 'pages/500.html', status=500)
