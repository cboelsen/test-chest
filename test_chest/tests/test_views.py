import pytest

from ..models import TestSuite as TS
from ..views import (
    UserViewSet,
    GroupViewSet,
    TagViewSet,
    TestCaseViewSet as TCVS,
    TestSuiteViewSet as TSVS,
)


@pytest.mark.django_db
def test_junit_xml_uploads(admin_client):
    with open('/mnt/sheeva/christian/tmp/pyTests.xml') as fp:
        res = admin_client.post('/testsuites/upload_junit_xml/', {'attachment': fp})
    print(res)
    assert TS.objects.count() == 1
