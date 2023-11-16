from django.db import models
from django.contrib.auth.models import User

# --- 회원 관련 ---

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_message  = models.TextField()
    git_address = models.URLField(max_length=30, default='')

    def __str__(self):
        return self.user.username

# --- fog 관련 model ---

class UploadedFile(models.Model):
    file = models.FileField(upload_to='before_fog/')
    upload_date = models.DateTimeField(auto_now_add=True)