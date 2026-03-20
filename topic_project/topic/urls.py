from django.urls import path
from topic_project.topic import views

app_name = "topic"

urlpatterns = [
    path("home/", views.index, name = "home"),
    path("register/", views.register, name = "register"),
    path("register/verify/", views.verify_email, name="verify_email"),
    path("register/resend/", views.resend_code, name="resend_code"),
    path("register/check-username/", views.check_username, name = "check_username"),
    path("register/check-email/", views.check_email, name = "check_email"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
]