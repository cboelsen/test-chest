import json
import pytest

from ..models import (
    Result,
    Tag,
    TestSuite as TS,
    TestCase as TC,
)
from ..views import (
    GroupViewSet,
    TagViewSet,
    TestCaseViewSet as TCVS,
    TestSuiteViewSet as TSVS,
    UserViewSet,
)


@pytest.mark.django_db
def test_junit_xml_uploads(admin_client):
    with open('tests/files/junit-1.xml') as fp:
        res = admin_client.post('/testsuites/upload_junit_xml/', {'attachment': fp})
    assert TS.objects.count() == 1
    assert TC.objects.count() == 3

    passed_tests = TC.objects.filter(result=Result.PASS)
    assert passed_tests.count() == 1
    assert passed_tests[0].message == None
    assert passed_tests[0].traceback == None
    assert passed_tests[0].testsuite == TS.objects.get()
    assert passed_tests[0].name == 'test_max_nodes'
    assert passed_tests[0].classname == "auto.platform-clustering.clusteringtests.test_cluster_join"
    assert passed_tests[0].time == 801.00904727
    assert passed_tests[0].file == "../../lib/python2.7/site-packages/clusteringtests/test_cluster_join.py"
    assert passed_tests[0].line == 15

    failed_tests = TC.objects.filter(result=Result.FAIL)
    assert failed_tests.count() == 1
    assert failed_tests[0].message == "CliCommandFailed: CliCommandFailed(rc=1, timestamp=2017-09-25T07:46:21.063509+01:00, output=The specified IP address is already in use)."
    assert 'def test_add_and_remove_ip_address_to_eth0(node, test_logger):' in failed_tests[0].traceback
    assert len(failed_tests[0].traceback.splitlines()) == 11

    skipped_tests = TC.objects.filter(result=Result.SKIP)
    assert skipped_tests.count() == 1
    assert skipped_tests[0].message == 'Investigate why this fails'
    assert skipped_tests[0].traceback == "../../lib/python2.7/site-packages/clusteringtests/test_cluster_unconfigure.py:8: <py._xmlgen.raw object at 0x7fa1ebfc2750>"
    assert len(skipped_tests[0].traceback.splitlines()) == 1


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
