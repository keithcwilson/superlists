import random
from fabric.api import env, local, run, cd
from fabric.context_managers import prefix
from os.path import join

REPO_URL = 'https://github.com/keithcwilson/superlists'


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()


def _get_latest_source():
    if '.git' in run("ls -a"):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')


def _update_virtualenv():
    if not 'bin' in run("ls -a virtualenv"):
        run(f'python3.9 -m venv virtualenv')
    with prefix(f'source virtualenv/bin/activate'):
        run('pip install -r requirements.txt')


def _create_or_update_dotenv():
    run('echo "DJANGO_DEBUG_FALSE=y" >> .env')
    run(f'echo "SITENAME={env.host}" >> .env')
    current_contents = run('cat .env', warn=True)
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices('abcdefghijklmnopqrstuvwxyz0123456789', k=50))
        run(f'echo "DJANGO_SECRET_KEY={new_secret}" >> .env')


def _update_static_files():
    with prefix(f'source virtualenv/bin/activate'):
        run('./manage.py collectstatic --noinput')


def _update_database():
    with prefix(f'source virtualenv/bin/activate'):
        run('./manage.py migrate --noinput')
