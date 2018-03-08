import subprocess

from .github_auth import github


def create_user_contribution_json(username):
    cmd = 'node index.js {} {}.json'.format(username)
    subprocess.call(cmd, shell=True)


def get_github_username(request):
    code = request.GET.get('code')
    auth_session = github.get_auth_session(data={'code': code})
    github_response = auth_session.get('/user')
    return github_response.json()['login']