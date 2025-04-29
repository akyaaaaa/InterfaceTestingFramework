from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import AuditLog

User = get_user_model()

class RegisterAPI(APIView):
    """用户注册API接口"""
    def post(self, request):
        """
        处理用户注册请求
        请求参数:
        - username: 用户名(必填)
        - password: 密码(必填)
        - email: 邮箱(可选)
        返回:
        - 成功: 201 Created 包含用户信息
        - 失败: 400 Bad Request 包含错误信息
        """
        try:
            # 获取请求数据
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email', '')

            # 基础验证
            if not username or not password:
                return Response(
                    {'error': '用户名和密码不能为空'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 创建用户
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            
            # 记录审计日志
            AuditLog.objects.create(
                user=user,
                action='REGISTER',
                ip_address=self.get_client_ip(request),
                details={
                    'method': 'API注册',
                    'username': username,
                    'email': email
                }
            )
            
            return Response({
                'status': 'success',
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'register_time': user.date_joined
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def get_client_ip(self, request):
        """获取客户端IP地址"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
