import json
import pytest

from ...models import (
    Result,
    TestSuite as TS,
    TestCase as TC,
)


@pytest.mark.django_db
def test_junit_xml_uploads(admin_client):
    with open('tests/files/junit-1.xml') as fp:
        admin_client.post('/testsuites/upload_junit_xml/', {'attachment': fp})
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
    assert passed_tests[0].tags.count() == 0

    failed_tests = TC.objects.filter(result=Result.FAIL)
    assert failed_tests.count() == 1
    assert failed_tests[0].message == "CliCommandFailed: CliCommandFailed(rc=1, timestamp=2017-09-25T07:46:21.063509+01:00, output=The specified IP address is already in use)."
    assert 'def test_add_and_remove_ip_address_to_eth0(node, test_logger):' in failed_tests[0].traceback
    assert len(failed_tests[0].traceback.splitlines()) == 11
    assert failed_tests[0].tags.count() == 0

    skipped_tests = TC.objects.filter(result=Result.SKIP)
    assert skipped_tests.count() == 1
    assert skipped_tests[0].message == 'Investigate why this fails'
    assert skipped_tests[0].traceback == "../../lib/python2.7/site-packages/clusteringtests/test_cluster_unconfigure.py:8: <py._xmlgen.raw object at 0x7fa1ebfc2750>"
    assert len(skipped_tests[0].traceback.splitlines()) == 1
    assert skipped_tests[0].tags.count() == 0


@pytest.mark.django_db
def test_junit_xml_uploads(admin_client):
    tags = ['tag1', 'tag2']
    with open('tests/files/junit-1.xml') as fp:
        admin_client.post('/testsuites/upload_junit_xml/', {'attachment': fp, 'tags': json.dumps(tags)})
    assert TS.objects.count() == 1
    assert TC.objects.count() == 3

    tests = TC.objects.all()
    assert tests[0].tags.count() == 2
    assert 'tag1' in tests[0].tags.values_list('name', flat=True)
    assert 'tag2' in tests[0].tags.values_list('name', flat=True)
    assert 'tag1' in tests[1].tags.values_list('name', flat=True)
    assert 'tag2' in tests[1].tags.values_list('name', flat=True)
    assert 'tag1' in tests[2].tags.values_list('name', flat=True)
    assert 'tag2' in tests[2].tags.values_list('name', flat=True)


@pytest.mark.django_db
def test_junit_xml_uploads_returned_json(admin_client):
    tags = ['tag1', 'tag2']
    with open('tests/files/junit-1.xml') as fp:
        res = admin_client.post('/testsuites/upload_junit_xml/', {'attachment': fp, 'tags': json.dumps(tags)})
    testsuites = res.json()
    assert len(testsuites) == 1
    from pprint import pprint
    pprint(testsuites)
