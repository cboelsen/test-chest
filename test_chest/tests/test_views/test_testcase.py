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
    return ts


@pytest.fixture
def testcase(testsuite):
    tc = TC(
        name='test1',
        classname='classname1',
        time=123,
        file='file1',
        line=1,
        testsuite=testsuite,
    )
    tc.save()
    return tc


@pytest.mark.django_db
def test_get_testsuites(client, testcase):
    results = json.loads(client.get('/testcases/').content.decode())
    assert results['count'] == 1


@pytest.mark.django_db
def test_post_testsuites(admin_client, testsuite):
    results = json.loads(admin_client.get('/testsuites/').content.decode())
    ts_url = results['results'][0]['url']
    tc = {
        'name': 'test2',
        'classname': 'classname2',
        'time': 123,
        'file': 'file2',
        'line': 12,
        'testsuite': ts_url,
    }
    response = admin_client.post('/testcases/', json.dumps(tc), content_type="application/json")
    assert response.status_code < 400
