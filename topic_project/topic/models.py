from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from typing import Any
from random import randint

# Create your models here.

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    


class EmailVerification(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.code:
            self.code = f"{randint(100000, 999999)}"
        super().save(*args, **kwargs)
    
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)