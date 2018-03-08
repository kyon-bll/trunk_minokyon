from django.shortcuts import render, redirect
from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'index/index.html'

    def get(self, request, *args, **kwargs):
        if 'username' not in request.session:
            return render(request, 'index/welcome.html')
        else:
            return super().get(request, *args, **kwargs)


def login(request):
    request.session['username'] = 'kyon'
    return redirect('index:index')
