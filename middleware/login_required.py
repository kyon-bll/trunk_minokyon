from re import compile

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import resolve_url

from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import REDIRECT_FIELD_NAME


EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware(MiddlewareMixin, object):
    """
    LOGIN_URL 以外のページでユーザ認証を要求するミドルウェア。
    ユーザ認証を免除するページは、 LOGIN_EXEMPT_URLS に正規表現で指定する
    必要がある。（これを urls.py にコピーすることもできる）
    ログイン要求ミドルウェアとコンテキストプロセッサーのテンプレートが
    読み込まれる。読み込まれなかった場合、エラーが発生するかもれない。
    """
    def process_request(self, request):
        assert hasattr(request, 'user'), "ログイン要求ミドルウェア\
はユーザ認証ミドルウェアのインストールを要求します。MIDDLEWARE_CLASSES を\
編集して、'django.contrib.auth.middlware.AuthenticationMiddleware' を\
追加してください。動作しない場合、 TEMPLATE_CONTEXT_PROCESSORS 設定が\
'django.core.context_processors.auth' に読み込まれていることを\
確認して下さい。"
        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                redirect_path = request.get_full_path()
                resolved_login_url = resolve_url(settings.LOGIN_URL)
                return redirect_to_login(
                    redirect_path, resolved_login_url, REDIRECT_FIELD_NAME)
