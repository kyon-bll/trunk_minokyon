from datetime import date
import urllib
from xml.etree import ElementTree

import qrcode

from .github_auth import github


def get_github_username(request):
    code = request.GET.get('code')
    auth_session = github.get_auth_session(data={'code': code})
    github_response = auth_session.get('/user')
    request.session['access_token'] = auth_session.access_token
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


def create_qrcode_images(request):
    url = (
        'http://localhost:8000/store/'
        '?username={}&rank={}&access_token={}&kind={}&date={}')

    for kind in ('コナモン', 'オモロイ', 'アツマロ'):
        img = qrcode.make(url.format(
            request.session['username'],
            request.session['geek_rank_name'],
            request.session['access_token'],
            kind, date.today()))
        img.save('static/img/qrcodes/{}_{}.png'.format(
            request.session['username'], kind))
