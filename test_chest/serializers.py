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
        fields = ('name', 'tests')


class TestCaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TestCase
        fields = (
            'id', 'name', 'classname', 'failure_message', 'traceback',
            'file', 'line', 'time', 'uploaded', 'additional', 'tags',
            'testsuite',
        )


class TestSuiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TestSuite
        fields = ('id', 'name', 'time', 'uploaded', 'tests')
