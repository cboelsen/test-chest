import json
import pytest

from ...models import (
    Tag,
    TestSuite as TS,
    TestCase as TC,
)


@pytest.fixture
def tags():
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
    tag1 = Tag(name='tag1')
    tag1.save()
    tag1.tests = [tc]
    tag1.save()
    tag2 = Tag(name='tag2')
    tag2.save()
    return tag1, tag2


@pytest.mark.django_db
def test_filter_tags__no_filter(client, tags):
    results = json.loads(client.get('/tags/').content.decode())
    assert results['count'] == 2


@pytest.mark.django_db
def test_filter_tags__tests_filter(client, tags):
    results = json.loads(client.get('/tags/?tests__name=test1').content.decode())
    assert results['count'] == 1
    assert results['results'][0]['name'] == 'tag1'


@pytest.mark.django_db
def test_filter_tags__limit_filter(client, tags):
    results = json.loads(client.get('/tags/?limit=1').content.decode())
    assert results['count'] == 2
    assert len(results['results']) == 1


@pytest.mark.django_db
def test_filter_tags__bad_filter(client, tags):
    response = client.get('/tags/?tests__blah=123')
    assert response.status_code == 400
