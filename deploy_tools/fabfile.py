import random
from pathlib import Path
from fabric import Connection, task

REPO_URL = 'https://github.com/keithcwilson/superlists'


@task
def deploy(c):
    site_folder = f'/home/{c.user}/sites/{c.host}'
    c.run(f'mkdir -p {site_folder}')
    with c.cd(site_folder):
        _get_latest_source(c)
        _update_virtualenv(c)
        _create_or_update_dotenv(c)
        _update_static_files(c)
        _update_database(c)


def _get_latest_source(c):
    if Path('.git').exists():
        c.run('git fetch')
    else:
        c.run(f'get clone {REPO_URL} .')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    c.run(f'git reset --hard {current_commit}')


def _update_virtualenv(c):
    if not Path('virtualenv/bin/pip').exists():
        c.run(f'python3.9 -m venv virtualenv')
    c.run('./virtualenv/bin/pip install -r requirements.txt')


def _create_or_update_dotenv(c):
    c.run('echo "DJANGO_DEBUG_FALSE=y" >> .env')
    c.run(f'echo "SITENAME={c.host}" >> .env')
    current_contents = c.run('cat .env', warn=True)
    if 'DJANGO_SECRET_KEY' not in current_contents.stdout:
        new_secret = ''.join(random.SystemRandom().choices('abcdefghijklmnopqrstuvwxyz0123456789', k=50))
        c.run(f'echo "DJANGO_SECRET_KEY={new_secret}" >> .env')


def _update_static_files(c):
    c.run('./virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database(c):
    c.run('./virtualenv/bin/python manage.py migrate --noinput')
