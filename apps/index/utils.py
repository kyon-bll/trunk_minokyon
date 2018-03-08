import urllib
from xml.etree import ElementTree

from .github_auth import github


def get_github_username(request):
    code = request.GET.get('code')
    auth_session = github.get_auth_session(data={'code': code})
    github_response = auth_session.get('/user')
    return github_response.json()['login']


def get_7days_user_contribution(username):
    url = 'https://github.com/users/{}/contributions'.format(username)
    req = urllib.request.Request(url)
    res = urllib.request.urlopen(req)
    svg = res.read()
    et = ElementTree.fromstring(svg)
    latest_7days_data = et.findall('./g/g/rect')[-7:]
    count = 0
    for data in latest_7days_data:
        count += int(data.get('data-count'))

    return count
