from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.
class User(AbstractUser):
    student_id = models.CharField(max_length=10, unique=True)
    is_student = models.BooleanField(default = False)
    def save(self, *args, **kwargs):
        if not self.student_id:
            self.student_id = str(uuid.uuid4()).replace('-','')[:10]
        super().save(*args, **kwargs)
    def __str__(self):
        return self.username
