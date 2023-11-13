from .views import (
    home,
    fog,
    community,
    contact,
    user_login,
    forgot_id,
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
    contact_detail,
    user_logout,
    forgot_id_result,

)
from django.urls import path

urlpatterns = [
    path("", home, name="home"),
    path("community", community, name="community"),
    path("contact", contact, name="contact"),
    
    path("post_form", post_form, name="post_form"),
    path("support", support, name="support"),
    path("about_us", about_us, name="about_us"),
    path("news_list", news_list, name="news_list"),
    path("news_detail", news_detail, name="news_detail"),
    path("user_profile", user_profile, name="user_profile"),
    path("admin_profile", admin_profile, name="admin_profile"),
    path("contact_list", contact_list, name="contact_list"),
    path("contact_detail", contact_detail, name="contact_detail"),
    # --- 회원관련 ---
    path("id_res", forgot_id_result, name="forgot_id_result"),
    path("user_login", user_login, name="user_login"),
    path("user_logout", user_logout, name="user_logout"),
    path("forgot_id", forgot_id, name="forgot_id"),
    path("forgot_id_result", forgot_id_result, name="forgot_id_result"),
    path("forgot_pw", forgot_pw, name="forgot_pw"),
    path("signup", signup, name="signup"),
    # --- fog ---
    path("fog", fog, name="fog"),
    
    # ========================== 아래는 페이지 확인 차 만든 것임. 삭제해도 됨! ===============================
    
]