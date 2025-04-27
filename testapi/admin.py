from django.contrib import admin
from .models import TestCase

@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'method', 'url')
    search_fields = ('name', 'category', 'url')
    list_filter = ('category', 'method')
