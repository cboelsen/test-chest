from django.contrib.auth.models import User, Group
from django.core.exceptions import FieldError

from rest_framework import filters, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

import xml.etree.ElementTree

from .models import Tag, TestCase, TestSuite, Result
from .serializers import (
    UserSerializer, GroupSerializer, TagSerializer, TestCaseSerializer,
    TestSuiteSerializer,
)


class FilteringModelViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        filters = self.request.query_params.dict().copy()
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
    queryset = Tag.objects.all().order_by('name').distinct()
    serializer_class = TagSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name')


class TestCaseViewSet(FilteringModelViewSet):
    queryset = TestCase.objects.all().order_by('uploaded')
    serializer_class = TestCaseSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = (
        'name', 'classname', 'file', 'line', 'time', 'uploaded', 'tags',
        'testsuite',
    )


class TestSuiteViewSet(FilteringModelViewSet):
    queryset = TestSuite.objects.all().order_by('uploaded')
    serializer_class = TestSuiteSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name', 'time', 'uploaded')

    @list_route(methods=['post'])
    def upload_junit_xml(self, request):
        suites = []
        for _, fp in request.FILES.items():
            e = xml.etree.ElementTree.fromstring(fp.read())
            xml_suites = list(e.findall('testsuite'))
            if not xml_suites:
                xml_suites = [e]
            for s in xml_suites:
                suite = TestSuite(name=s.get('name'), time=s.get('time'))
                suite.save()
                for c in s.findall('testcase'):
                    tc = TestCase(
                        name=c.get('name'),
                        classname=c.get('classname'),
                        time=c.get('time'),
                        file=c.get('file'),
                        line=c.get('line'),
                        testsuite=suite,
                    )
                    # TODO: XFAIL, ERROR...
                    failure = c.find('failure')
                    skipped = c.find('skipped')
                    if failure is not None:
                        tc.result = Result.FAIL
                        tc.message = failure.get('message')
                        tc.traceback = failure.text
                    elif skipped is not None:
                        tc.result = Result.SKIP
                        tc.message = skipped.get('message')
                        tc.traceback = skipped.text
                    else:
                        tc.result = Result.PASS
                    tc.save()
                suites.append(suite)
        return Response(TestSuiteSerializer(suites, context={'request': request}, many=True).data)
