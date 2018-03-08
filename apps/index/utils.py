import json
import subprocess

from .github_auth import github


def create_user_contribution_json(username):
    cmd = 'node {scraper} {username} {output_dir}{username}.json'.format(
        username=username,
        scraper='github-contributions-scraper/index.js',
        output_dir='user_contributions/')
    subprocess.call(cmd, shell=True)


def get_github_username(request):
    code = request.GET.get('code')
    auth_session = github.get_auth_session(data={'code': code})
    github_response = auth_session.get('/user')
    return github_response.json()['login']


def get_7days_user_contribution(username):
    user_json = open('user_contributions/{}.json'.format(username), 'r')
    contributions_list = json.load(user_json)
    count = 0
    for i, day in enumerate(reversed(contributions_list)):
        if i == 7:
            break
        count += day['count']

    return count
