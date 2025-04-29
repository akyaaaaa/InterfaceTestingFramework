from .models import AuditLog
from django.utils import timezone
from django.contrib.auth import get_user

class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # 排除静态文件和管理后台请求
        if request.path.startswith('/admin') or request.path.startswith('/static'):
            return response
            
        try:
            user = get_user(request)
            if not user.is_authenticated:
                user = None
        except:
            user = None

        # 记录审计日志
        AuditLog.objects.create(
            user=user,
            action='API_REQUEST',
            ip_address=self.get_client_ip(request),
            object_type=request.path,
            details={
                'method': request.method,
                'params': dict(request.GET),
                'status_code': response.status_code
            }
        )
        
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
