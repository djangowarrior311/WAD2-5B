from django.urls import path
from topic_project.topic import views

app_name = "topic"

urlpatterns = [
    path("home/", views.index, name = "home"),
    path("home/get_tags", views.get_tags, name="get_tags"),
    path("home/get_search_results", views.get_search_results, name="get_search_results"),
    path("register/", views.register, name = "register"),
    path("register/verify/", views.verify_email, name="verify_email"),
    path("register/resend/", views.resend_code, name="resend_code"),
    path("register/check-username/", views.check_username, name = "check_username"),
    path("register/check-email/", views.check_email, name = "check_email"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("tools/<slug:learning_tool_slug>/", views.show_tool, name="show_tool"),
    path("tools/<slug:learning_tool_slug>/add_review/", views.add_review, name="add_review"),
]