import pytest
import uuid

from ..models import Tag, TestCase as TC, TestSuite as TS


@pytest.fixture
def ts_id():
    return uuid.UUID('5ae46e97-ab17-403e-838c-b8230a6393a1')


@pytest.fixture
def testsuite(ts_id):
    ts = TS(id=ts_id, name='suite1', time=123.0)
    return ts


@pytest.fixture
def tc_id():
    return uuid.UUID('5ae46e97-ab17-403e-838c-b8230a6393a1')


@pytest.fixture
def testcase(testsuite, tc_id):
    return TC(
        id=tc_id,
        name='test1',
        classname='class1',
        file='f',
        line=12,
        time=1.2,
        testsuite=testsuite,
    )


@pytest.mark.django_db
def test_tag_text_representation():
    tag = Tag(name='blah')
    assert str(tag) == 'Tag(blah)'


@pytest.mark.django_db
def test_testsuite_text_representation(testsuite):
    assert str(testsuite) == 'TestSuite(suite1, 5ae46e97-ab17-403e-838c-b8230a6393a1)'


@pytest.mark.django_db
def test_testcase_text_representation(testsuite, testcase):
    assert str(testcase) == 'TestCase(class1.test1, 5ae46e97-ab17-403e-838c-b8230a6393a1)'


@pytest.mark.django_db
def test_tag_test_case_many_to_many_relationship(testsuite, testcase):
    testcase.save()
    tag = Tag(name='tag1')
    tag.save()
    tag.tests=[testcase]
