from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from pathlib import Path

def upload_to(instance, filename):
    ext = Path(filename).suffix.lower()
    return f'uploads/{uuid4().hex}{ext}'

class UploadRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)
