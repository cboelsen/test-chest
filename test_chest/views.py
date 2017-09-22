from django.contrib.auth.models import User, Group
from django.core.exceptions import FieldError

from rest_framework import filters, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.exceptions import ParseError

import xml.etree.ElementTree

from .models import Tag, TestCase, TestSuite
from .serializers import (
    UserSerializer, GroupSerializer, TagSerialiser, TestCaseSerialiser,
    TestSuiteSerialiser,
)


class FilteringModelViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        filters = self.request.query_params.dict()
        for filter_name in ['ordering', 'limit', 'offset']:
            if filter_name in filters:
                del filters[filter_name]
        try:
            return self.queryset.filter(**filters).distinct()
        except FieldError as error:
            raise ParseError(error.args)


class UserViewSet(FilteringModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('date_joined')


class GroupViewSet(FilteringModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id')


class TagViewSet(FilteringModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerialiser
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name')


class TestCaseViewSet(FilteringModelViewSet):
    queryset = TestCase.objects.all().order_by('uploaded')
    serializer_class = TestCaseSerialiser
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = (
        'name', 'classname', 'file', 'line', 'time', 'uploaded', 'tags',
        'testsuite',
    )


class TestSuiteViewSet(FilteringModelViewSet):
    queryset = TestSuite.objects.all().order_by('uploaded')
    serializer_class = TestSuiteSerialiser
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name', 'time', 'uploaded')

    @list_route(methods=['post'])
    def upload_junit_xml(self, request):
        suites = []
        for xml_file in request.FILES:
            e = xml.etree.ElementTree.fromstring(xml_file.read()).getroot()
            if isinstance(xml, JUnitXmlWithString):
                suites = [s for s in xml]
            else:
                suites = [xml]
            for s in e.findall('testsuite'):
                suite = TestSuite(name=s.get('name'), time=s.get('time'))
                suite.save()
                for c in s.findall('testcase'):
                    # TODO: Parse <failure message=""> and get traceback
                    TestCase(
                        name=c.get('name'),
                        classname=c.get('classname'),
                        time=c.get('time'),
                        file=c.get('file'),
                        line=c.get('line'),
                        testsuite=suite,
                    ).save()
            suites.append(suite)
        return Response(TestSuiteSerializer(suites, many=True).data)
