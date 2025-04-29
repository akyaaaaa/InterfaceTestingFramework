from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from apps.audit.models import AuditLog
from rest_framework_simplejwt.tokens import RefreshToken

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
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email', '')

            if not username or not password:
                return Response(
                    {'error': '用户名和密码不能为空'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            
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
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

import logging
logger = logging.getLogger('apps.auth.views')
from rest_framework.permissions import AllowAny
class LoginAPI(APIView):
    """用户登录API接口"""
    permission_classes = [AllowAny]
    def post(self, request):
        """
        处理用户登录请求
        请求参数:
        - username: 用户名(必填)
        - password: 密码(必填)
        返回:
        - 成功: 200 OK 包含访问令牌
        - 失败: 401 Unauthorized
        """
        logger.debug("\n==== 请求调试开始 ====")
        logger.debug("1. 原始请求数据: %s", request.body)
        logger.debug("2. 请求头: %s", dict(request.headers))
        logger.debug("3. 解析后的数据: %s", request.data)
        
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            logger.debug("4. 获取到的用户名: %s", username)
            logger.debug("5. 获取到的密码: %s", password) 
            logger.debug("6. 用户存在: %s", User.objects.filter(username=username).exists())
            logger.debug("解析后的数据 - 用户名:%s, 密码:%s", username, password)

            if not username or not password:
                logger.warning("用户名或密码为空")
                return Response(
                    {'error': '用户名和密码不能为空'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = authenticate(username=username, password=password)
            logger.debug(f"认证结果：{user}")

            if not user:
                logger.warning(f"认证失败 - 用户名:{username} 密码:{password} 用户存在:{User.objects.filter(username=username).exists()}")
                return Response(
                    {
                        'error': '用户名或密码错误',
                        'detail': '请检查用户名和密码是否正确'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # 生成JWT令牌
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            # 记录审计日志
            AuditLog.objects.create(
                user=user,
                action='LOGIN',
                ip_address=self.get_client_ip(request),
                details={
                    'method': 'API登录',
                    'username': username
                }
            )
            
            return Response({
                'status': 'success',
                'user_id': user.id,
                'username': user.username,
                'access_token': access_token,
                'refresh_token': str(refresh)
            })
            
        except Exception as e:
            logger.error(f"登录过程中发生异常: {str(e)}")
            return Response(
                {'error': '服务器内部错误'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_client_ip(self, request):
        """获取客户端IP地址"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
