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

    def __str__(self):
        return self.name



# this is for Syon's review system, which is separate from the tool form
#@login_required
class Review(models.Model):
    learningtool = models.ForeignKey(LearningTool, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_authored')
    rating = models.FloatField(default=0.0) 
    sentence = models.CharField(max_length=256, blank=True) 

    def __str__(self):
        return f"review by {self.author.username} for {self.learningtool.name}"
    
