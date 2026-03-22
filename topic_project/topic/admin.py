from django.contrib import admin
from topic_project.topic.models import Tag, LearningTool, Review

# Register your models here.

admin.site.register(Tag)
admin.site.register(LearningTool)
admin.site.register(Review)