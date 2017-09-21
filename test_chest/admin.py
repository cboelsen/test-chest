from django.contrib import admin
from .models import Tag, TestCase, TestSuite


class TagAdmin(admin.ModelAdmin):
    pass


class TestCaseAdmin(admin.ModelAdmin):
    pass


class TestSuiteAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag, TagAdmin)
admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(TestSuite, TestSuiteAdmin)
