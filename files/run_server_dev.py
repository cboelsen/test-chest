import django
import os
import subprocess
import sys
import time


def test_db_connection():
    conn = django.db.connections['default']
    conn.cursor()


def wait_for_connection():
    while True:
        try:
            test_db_connection()
            return
        except django.db.utils.OperationalError:
            pass
        time.sleep(0.5)


def migrate_to_latest_models():
    settings = ['--settings', os.environ['DJANGO_SETTINGS_MODULE']]
    cmd = '/var/lib/test-chest-env/bin/test-chest'
    # PRODUCTION VERSION:
    # subprocess.check_call([cmd, 'makemigrations', '--check', '--noinput'] + settings)
    subprocess.check_call([cmd, 'makemigrations', '--noinput'] + settings)
    subprocess.check_call([cmd, 'migrate', '--noinput'] + settings)


def create_test_user():
    from django.contrib.auth.models import User
    u, _ = User.objects.get_or_create(username='test')
    u.set_password('test')
    u.is_staff = True
    u.save()


def run_nginx_in_background():
    os.mkdir('/run/nginx')
    subprocess.Popen(['nginx'])


def run_supervisor():
    return subprocess.call(['supervisord', '-c', '/etc/supervisor/supervisord.conf'])


def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'test_chest_project.test_chest_project.settings.dev'
    django.setup()
    wait_for_connection()
    migrate_to_latest_models()
    create_test_user()
    run_nginx_in_background()
    return run_supervisor()


if __name__ == "__main__":
    sys.exit(main())
