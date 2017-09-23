import pytest
import uuid

from ..models import Tag, TestCase as TC, TestSuite as TS


@pytest.fixture
def testsuite():
    ts = TS(name='suite1', time=123.0)
    return ts


@pytest.mark.django_db
def test_tag_text_representation():
    tag = Tag(name='blah')
    assert str(tag) == 'Tag(blah)'


@pytest.mark.django_db
def test_testsuite_text_representation():
    ts_id = uuid.UUID('5ae46e97-ab17-403e-838c-b8230a6393a1')
    ts = TS(id=ts_id, name='suite1')
    assert str(ts) == 'TestSuite(suite1, 5ae46e97-ab17-403e-838c-b8230a6393a1)'


@pytest.mark.django_db
def test_testcase_text_representation(testsuite):
    tc_id = uuid.UUID('5ae46e97-ab17-403e-838c-b8230a6393a1')
    tc = TC(
        id=tc_id,
        name='test1',
        classname='class1',
        file='f',
        line=12,
        time=1.2,
        testsuite=testsuite,
    )
    assert str(tc) == 'TestCase(class1.test1, 5ae46e97-ab17-403e-838c-b8230a6393a1)'
