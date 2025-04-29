from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from .models import AuditLog
import inspect

"""
本文件作用，记录"谁修改了哪些数据，从什么值改成什么值"
Django提供了一些内置信号，也可以自定义信号。以下是常用内置信号：

django.db.models.signals.pre_save：在模型对象保存之前触发。
django.db.models.signals.post_save：在模型对象保存之后触发。
django.db.models.signals.pre_delete：在模型对象删除之前触发。
django.db.models.signals.post_delete：在模型对象删除之后触发

"""
User = get_user_model()
"""
使用 inspect.stack() 检查调用栈，找到包含 request 对象的帧。
如果 request 存在且有 user 属性，则返回当前用户。
如果找不到用户（例如后台脚本或非 HTTP 请求），返回 None。
"""
def get_current_user():
    """获取当前操作用户"""
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals.get('request')
            if request and hasattr(request, 'user'):
                return request.user
    return None

# 信号处理器
@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    if not hasattr(instance._meta, 'auditlog'):  # 检查表是否存在
        return
    # 跳过AuditLog模型，避免无线递归
    if sender._meta.label == 'audit.AuditLog':
        return
    # AnonymousUser表示匿名用户
    user = get_current_user() or AnonymousUser()
    # 保存之后触发，只有可能为创建或更新
    action = 'CREATE' if created else 'UPDATE'
    
    AuditLog.objects.create(
        # isinstance(user, AnonymousUser)检查user是否是AnonymousUser对象
        user=user if not isinstance(user, AnonymousUser) else None,
        action=action,
        object_type=sender._meta.label,
        object_id=str(instance.pk),
        details={
            'fields': {f.name: str(getattr(instance, f.name)) 
                      for f in sender._meta.fields}
        }
    )

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender._meta.label == 'audit.AuditLog':
        return
        
    user = get_current_user() or AnonymousUser()
    
    AuditLog.objects.create(
        user=user if not isinstance(user, AnonymousUser) else None,
        action='DELETE',
        object_type=sender._meta.label,
        object_id=str(instance.pk),
        details={
            'deleted_object': str(instance)
        }
    )
