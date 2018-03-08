import math

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
            self.contribution = utils.get_7days_user_contribution(self.username)
            return super().get(request, *args, **kwargs)

    # context
    @property
    def geek_point(self):
        return round(self.contribution ** math.log(530000, 70))

    @property
    def geek_rank(self):
        if self.geek_point == 0:
            return 0  # 0
        elif self.geek_point < 5000:
            return 1  # 1 - 15
        elif self.geek_point < 100000:
            return 2  # 16 - 40
        elif self.geek_point < 530000:
            return 3  # 40 - 69
        else:
            return 4  # 70 -

    @property
    def geek_rank_name(self):
        if self.geek_rank == 0:
            return 'ぎーくやあらへん'
        elif self.geek_rank == 1:
            return 'しょしんしゃぎーく'
        elif self.geek_rank == 2:
            return 'そこそこぎーく'
        elif self.geek_rank == 3:
            return 'いっちょまえぎーく'
        elif self.geek_rank == 4:
            return 'どえらいぎーく！！'


# github から返ってきたコードを用いて、
# access トークン取得
# ユーザー名を セッション に保存
def callback(request):
    request.session['username'] = utils.get_github_username(request)
    return redirect('index:index')


def logout(request):
    request.session.clear()
    return redirect('index:index')
