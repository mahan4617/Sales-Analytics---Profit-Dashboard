from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from pathlib import Path

def upload_to(instance, filename):
    ext = Path(filename).suffix.lower()
    return f'uploads/{uuid4().hex}{ext}'

class Upload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_to)
    original_name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    size = models.BigIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

class StoreProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='store_profile')
    store_name = models.CharField(max_length=255)
