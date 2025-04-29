from django.db import models
from django.contrib.auth import get_user_model

# 相比于from django.contrib.auth.models import User，下面地方法会更加灵活地获取用户
User = get_user_model()
"""
创建了一张AuditLog表,外键(use)连接到User,有字段action,ip_address,object_type,object_id,timestamp,details
"""
class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', '创建'),
        ('UPDATE', '修改'), 
        ('DELETE', '删除'),
        ('RUN', '执行'),
        ('LOGIN', '登录'),
        ('LOGOUT', '登出')
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='用户'
    )
    action = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES,
        verbose_name='操作类型'
    )
    ip_address = models.GenericIPAddressField(
        verbose_name='IP地址'
    )
    object_type = models.CharField(
        max_length=100,
        verbose_name='对象类型'
    )
    object_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='对象ID'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='时间戳'
    )
    details = models.JSONField(
        default=dict,
        verbose_name='详情'
    )

    class Meta:
        verbose_name = '审计日志'
        verbose_name_plural = verbose_name
        ordering = ['-timestamp']
        # 展示内容的排序规则
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['action']),
            models.Index(fields=['object_type', 'object_id']),
        ]

    def __str__(self):
        return f"{self.get_action_display()} - {self.object_type} by {self.user}"
