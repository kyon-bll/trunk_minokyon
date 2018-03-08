from django.shortcuts import render, redirect
from django.views import generic

from .github_auth import github
from . import utils


# 描画全部この子がやる
class IndexView(generic.TemplateView):
    template_name = 'index/index.html'

    def get(self, request, *args, **kwargs):
        if 'username' not in request.session:
            context = dict(authorize_url=github.get_authorize_url())
            return render(request, 'index/welcome.html', context)
        else:
            self.username = request.session['username']
            utils.create_user_contribution_json(self.username)
            return super().get(request, *args, **kwargs)

    # context
    @property
    def geek_point(self):
        pass


# github から返ってきたコードを用いて、
# access トークン取得
# ユーザー名を セッション に保存
def callback(request):
    request.session['username'] = utils.get_github_username(request)
    return redirect('index:index')


def logout(request):
    request.session.clear()
    return redirect('index:index')
