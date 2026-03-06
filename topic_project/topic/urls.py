from django.urls import path
from topic import views

app_name = "topic"

urlpatterns = [
    path("register/", views.register, name = "register"),
]