from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.forms import AuthenticationForm

urlpatterns = [
    url(r'^$', views.StoreIndexView.as_view(), name='index'),
    url(r'^login/$',
        auth_views.login,
        {'template_name': 'store/login.html',
         'authentication_form': AuthenticationForm,
         'extra_context': {'title': '店舗ログイン'}},
        name='login'),
    url(r'^logout/$',
        # ログアウト後ログインページへリダイレクト
        auth_views.logout_then_login,
        name='logout'),
]
