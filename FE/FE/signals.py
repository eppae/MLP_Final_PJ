# User 객체가 생성될 때마다 자동으로 UserProfile(aboutus/admin-profile을 위해)을 생성하도록 신호를 설정!
# Django에서 User를 이용하고 사용자설정 column을 만들고 싶을 때 사용하면 좋을듯??
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # 새 User 객체에 대해 Profile 객체 생성
        Profile.objects.create(user=instance)
    else:
        # 기존 User 객체 업데이트 시 Profile도 저장
        instance.profile.save()