from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from .models import AuditLog
import inspect

User = get_user_model()

def get_current_user():
    """获取当前操作用户"""
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals.get('request')
            if request and hasattr(request, 'user'):
                return request.user
    return None

@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    if sender._meta.label == 'audit.AuditLog':
        return
        
    user = get_current_user() or AnonymousUser()
    action = 'CREATE' if created else 'UPDATE'
    
    AuditLog.objects.create(
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
