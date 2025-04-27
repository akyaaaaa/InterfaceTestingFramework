from django.db import models
from django.db.models import JSONField

class TestCase(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    method = models.CharField(max_length=10)
    url = models.CharField(max_length=255) 
    body = JSONField(null=True, blank=True)
    expected_status_code = models.IntegerField()
    expected_response = JSONField(null=True, blank=True)
    root_url = models.CharField(max_length=255, default='https://reqres.in')

    def __str__(self):
        return self.name
