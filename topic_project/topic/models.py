from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class LearningTool(models.Model):
    CATEGORIES = (
        ('AI', 'AI'),
        ('NOTE', 'Note Taking'),
        ('FLASH', 'Flashcard'),
        ('OTHER', 'Other'),
    )
    
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=5, choices=CATEGORIES, default='OTHER')
    link = models.URLField()
    score = models.FloatField(default=0.0)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='createdtools')
    likes = models.ManyToManyField(User, related_name='likedtools', blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(LearningTool, self).save(*args, **kwargs)
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



class Tag(models.Model):
    TAG_NAME_MAX_LENGTH = 128

    name = models.CharField(max_length=TAG_NAME_MAX_LENGTH, unique=True)

    def __str__(self):
        return self.name

class Tool(models.Model):
    TOOL_NAME_MAX_LENGTH = 128

    name = models.CharField(max_length=TOOL_NAME_MAX_LENGTH, unique=True)
    url = models.URLField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Review(models.Model):
    REVIEW_MAX_LENGTH = 2000
    RATING_CHOICES = (
        (1,"*"),
        (2,"**"),
        (3,"***"),
        (4,"****"),
        (5,"*****"),
    )

    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES, default=None)
    review_content = models.TextField(max_length=REVIEW_MAX_LENGTH)

    def __str__(self):
        return self.review_content
