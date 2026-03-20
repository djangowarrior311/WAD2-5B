from django.contrib import admin
from topic_project.topic.models import Tag, Tool, Review

# Register your models here.

admin.site.register(Tag)
admin.site.register(Tool)
admin.site.register(Review)