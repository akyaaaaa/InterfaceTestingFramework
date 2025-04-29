from django.apps import AppConfig

class AuditConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.audit'
    verbose_name = '审计日志'

    def ready(self):
        # 注册信号处理器
        from . import signals  # noqa
