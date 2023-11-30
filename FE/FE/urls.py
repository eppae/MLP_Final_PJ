from .views import (
    home,
    fog,
    community,
    contact,
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
    contact_list_category,
    contact_detail,
    submit_contact,
    delete_contact,
    create_post,
    n_category_news_list,
    # fog_result,   모델 만들어지면 예정
    review_detail,
    
    forgot_id_result,
    user_login,
    user_logout,
    # change_profile_info,
    # change_profile_picture,
    
)
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", home, name="home"),
    path("community", community, name="community"),
    path("contact", contact, name="contact"),
    path("post_form", post_form, name="post_form"),
    path("support", support, name="support"),
    path("review_detail", review_detail, name="review_detail"),
    path("news_list", news_list, name="news_list"),
    path("news_detail", news_detail, name="news_detail"),
        # --- 회원관련 ---
    path("about_us", about_us, name="about_us"),
    path("id_res", forgot_id_result, name="forgot_id_result"),
    path("user_login", user_login, name="user_login"),
    path("user_logout", user_logout, name="user_logout"),
    path("forgot_id", forgot_id, name="forgot_id"),
    path("forgot_id_result", forgot_id_result, name="forgot_id_result"),
    path("forgot_pw", forgot_pw, name="forgot_pw"),
    path("signup", signup, name="signup"),
    path("user_profile", user_profile, name="user_profile"),
    path("admin_profile", admin_profile, name="admin_profile"),
    # path("change_profile_picture", change_profile_picture, name="change_profile_picture"),
    # path("change_profile_info", change_profile_info, name="change_profile_info"),
    # --- fog ---
    path("fog/", fog, name="fog"),

# ========================== contact BE url ===============================
    path('submit_contact', submit_contact, name='submit_contact'),
    path("contact_list", contact_list, name="contact_list"),
    path("contact_list/<str:category>/", contact_list_category, name="contact_list_category"),
    path("contact_detail/<int:post_num>/", contact_detail, name="contact_detail"),
    path("delete_contact", delete_contact, name="delete_contact"),
    path("create_post", create_post, name="create_post"),
    path("news_list/<str:n_category>/", n_category_news_list, name="news_list_category"),
    # path("fog_result", fog_result, name="fog_result"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)