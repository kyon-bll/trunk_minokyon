from django.shortcuts import render, redirect
from django.views import generic

from .github_auth import github


class IndexView(generic.TemplateView):
    template_name = 'index/index.html'

    def get(self, request, *args, **kwargs):
        if 'username' not in request.session:
            context = dict(authorize_url=github.get_authorize_url())
            return render(request, 'index/welcome.html', context)
        else:
            return super().get(request, *args, **kwargs)


def callback(request):
    request.session['username'] = 'kyon'
    return redirect('index:index')


def logout(request):
    request.session.clear()
    return redirect('index:index')
