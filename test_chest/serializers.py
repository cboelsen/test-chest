from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Tag, TestCase, TestSuite


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('url', 'name', 'tests')


class TestCaseSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = TestCase
        fields = (
            'url', 'id', 'name', 'classname', 'message', 'traceback', 'file',
            'line', 'time', 'uploaded', 'additional', 'tags', 'testsuite',
        )


class TestSuiteSerializer(serializers.HyperlinkedModelSerializer):
    tests = TestCaseSerializer(many=True, read_only=True)

    class Meta:
        model = TestSuite
        fields = ('url', 'id', 'name', 'time', 'uploaded', 'tests')
