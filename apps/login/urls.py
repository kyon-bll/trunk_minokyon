from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    url(r'$',
        auth_views.login,
        {'template_name': 'login/login.html',
         'authentication_form': LoginForm,
         'extra_context': {'title': 'ログイン'}},
        name='login'),
    url(r'out/$',
        # ログアウト後ログインページへリダイレクト
        auth_views.logout_then_login,

        # ログアウトページ表示
        # auth_views.logout,
        # {'template_name': 'login/logout.html'},
        name='logout'),
]
