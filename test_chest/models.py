import uuid

from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return 'Tag("{}")'.format(self.name)


class TestSuite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    time = models.FloatField()
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'TestSuite({}, {})'.format(self.name, self.id)


class TestCase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    classname = models.CharField(max_length=255)
    file = models.CharField(max_length=255)
    line = models.PositiveIntegerField()
    time = models.FloatField()
    uploaded = models.DateTimeField(auto_now_add=True)

    failure_message = models.TextField(null=True, blank=True)
    traceback = models.TextField(null=True, blank=True)

    tags = models.ManyToManyField(Tag, related_name='tests')
    testsuite = models.ForeignKey(TestSuite, related_name='tests')

    def __str__(self):
        return 'TestCase({}.{}, {})'.format(self.classname, self.name, self.id)
