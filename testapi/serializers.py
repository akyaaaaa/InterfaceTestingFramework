from rest_framework import serializers
from .models import TestCase

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        # 创建用例的序列化对象
        model = TestCase
        fields = '__all__'
