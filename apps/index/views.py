from django.shortcuts import render, redirect
from django.views import generic

from .github_auth import github


# 描画全部この子
class IndexView(generic.TemplateView):
    template_name = 'index/index.html'

    def get(self, request, *args, **kwargs):
        if 'username' not in request.session:
            context = dict(authorize_url=github.get_authorize_url())
            return render(request, 'index/welcome.html', context)
        else:
            return super().get(request, *args, **kwargs)


# github から返ってきたコードを用いて、
# access トークン取得
# ユーザー名を セッション に保存
def callback(request):
    code = request.GET.get('code')
    auth_session = github.get_auth_session(data={'code': code})
    github_response = auth_session.get('/user')
    request.session['username'] = github_response.json()['login']
    return redirect('index:index')


def logout(request):
    request.session.clear()
    return redirect('index:index')
