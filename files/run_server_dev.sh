#!/bin/bash

dbcheck() {
    alias db-check='test-chest shell -c "from django.db import connections;conn = connections['default']; conn.cursor()" >& /dev/null'
}

dbcheck
while [[ 0 -ne $? ]]; do
    sleep 1
    dbcheck
done

test-chest makemigrations --check --noinput --settings test_chest_project.test_chest_project.settings.dev
test-chest migrate --noinput --settings test_chest_project.test_chest_project.settings.dev

test-chest shell -c "from django.contrib.auth.models import User; u, _ = User.objects.get_or_create(username='test'); u.set_password('test'); u.is_staff = True; u.save()" --settings test_chest_project.test_chest_project.settings.dev

nginx &

supervisord -c /etc/supervisor/supervisord.conf
