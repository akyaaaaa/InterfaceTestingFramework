from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
# 创建新用户：python manage.py test apps.audit.tests.AuditTests.setUpTestData
class AuditTests(TestCase):
  def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='test11',  # 直接指定用户名
            password='123456',
            email='test@example.com'
        )
        self.assertIsNotNone(user.id)  # 验证用户创建成功
        self.assertFalse(user.is_staff)  # 验证是非管理员用户
    