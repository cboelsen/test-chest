import json
import pytest

from ...models import (
    TestSuite as TS,
    TestCase as TC,
)


@pytest.fixture
def testsuite():
    ts = TS(name='suite1', time=123)
    ts.save()
    tc = TC(
        name='test1',
        classname='classname1',
        time=123,
        file='file1',
        line=1,
        testsuite=ts,
    )
    tc.save()
    return TS.objects.first()


@pytest.mark.django_db
def test_get_testsuites(client, testsuite):
    results = json.loads(client.get('/testsuites/').content.decode())
    assert results['count'] == 1


@pytest.mark.django_db
def test_post_testsuites(admin_client):
    ts = {'name': 'suite1', 'time': 123, 'tests': []}
    response = admin_client.post('/testsuites/', json.dumps(ts), content_type="application/json")
    assert response.status_code < 400
