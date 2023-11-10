from .views import (
    home,
    fog,
    community,
    contact,
    login,
    forgot_pw,
    signup,
    post_form,
    support,
    about_us,
    news_list,
    news_detail,
    user_profile,
    admin_profile,
    contact_list,
    contact_detail
)
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("", home, name="home"),
    path("fog", fog, name="fog"),
    path("community", community, name="community"),
    path("contact", contact, name="contact"),
    path("login", login, name="login"),
    path("forgot_pw", forgot_pw, name="forgot-password"),
    path("signup", signup, name="signup"),
    path("post_form", post_form, name="post_form"),
    path("support", support, name="support"),
    path("about_us", about_us, name="about_us"),
    path("news_list", news_list, name="news_list"),
    path("news_detail", news_detail, name="news_detail"),
    path("user_profile", user_profile, name="user_profile"),
    path("admin_profile", admin_profile, name="admin_profile"),
    path("contact_list", contact_list, name="contact_list"),
    path("contact_detail", contact_detail, name="contact_detail"),
]