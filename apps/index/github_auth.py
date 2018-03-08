from django.conf import settings

from rauth import OAuth2Service

github = OAuth2Service(
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    name='github',
    authorize_url='https://github.com/login/oauth/authorize',
    access_token_url='https://github.com/login/oauth/access_token',
    base_url='https://api.github.com/')
