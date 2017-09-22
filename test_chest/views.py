from django.contrib.auth.models import User, Group
from rest_framework import filters, viewsets

from .models import Tag, TestCase, TestSuite
from .serializers import (
    UserSerializer, GroupSerializer, TagSerialiser, TestCaseSerialiser,
    TestSuiteSerialiser,
)


class FilteringModelViewSet(viewsets.ModelViewSet):

    # def get_serializer_context(self):
    #     return {
    #         'request': None,
    #         'format': self.format_kwarg,
    #         'view': self,
    #     }

    def get_queryset(self):
        filters = self.request.query_params.dict()
        build_query = Q()
        for filter_name in ['ordering', 'limit', 'offset']:
            if filter_name in filters:
                del filters[filter_name]
        return self.queryset.filter(build_query, **filters).distinct()


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
