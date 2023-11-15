from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='before_fog/')
    upload_date = models.DateTimeField(auto_now_add=True)