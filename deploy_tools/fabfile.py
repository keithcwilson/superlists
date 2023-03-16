import random
from fabric.operations import
from fabric.api import cd, env, local, run

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
    if run('.git').ok:
        run('git fetch')
    else:
        run(f'get clone {REPO_URL} .')
        current_commit = local("git log -n 1 --format=%H", capture=True)
        run(f'git reset --hard {current_commit}')


def _update_virtualenv():
    if not run('virtualenv/bin/pip').ok:
        run(f'python3.9 -m venv virtualenv')
    run('./virtualenv/bin/pip install -r requirements.txt')


def _create_or_update_dotenv():
    run('echo "DJANGO_DEBUG_FALSE=y" >> .env')
    run(f'echo "SITENAME={env.host}" >> .env')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices('abcdefghijklmnopqrstuvwxyz0123456789', k=50))
        run(f'echo "DJANGO_SECRET_KEY={new_secret}" >> .env')


def _update_static_files():
    run('./virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database():
    run('./virtualenv/bin/python manage.py migrate --noinput')
