from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# --- 회원 관련 ---

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_message  = models.TextField()
    git_address = models.URLField(max_length=30, default='')
    profile_picture = models.ImageField(upload_to='profile/', default='profile/default.jpg')
    dateTimeOfUpload = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

# --- fog 관련 model ---

class UploadedFile(models.Model):
    file = models.FileField(upload_to='after_fog/')
    upload_date = models.DateTimeField(auto_now_add=True)
    
class dehazing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to='before_fog/')
    processed_image = models.ImageField(upload_to='after_fog/', null=True, blank=True)
    # original_video = models.FileField(upload_to='before_fog/')
    # processed_video = models.FileField(upload_to='after_fog/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

# --- contact 모델 ---
class ContactMessage(models.Model):
    post_num = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, default='normal')
    def __str__(self):
        return f"{self.title}"

class PostForm(models.Model):
    post_num = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    img = models.ImageField(upload_to='img', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, default='normal')
    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(PostForm, on_delete=models.CASCADE)
    parentcomment = models.ForeignKey('self',on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.content}"
    class Meta:
        ordering = ["-created_at"]
