from django.apps import AppConfig

class UserAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.auth'
    label = 'user_auth'  # 添加唯一标签避免冲突
