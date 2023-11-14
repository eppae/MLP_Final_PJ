from django.shortcuts import render


def home(request):
    return render(request, "pages/home.html")


def fog(request):
    return render(request, "pages/test/fog.html")


def community(request):
    return render(request, "pages/community/community.html")


def contact(request):
    return render(request, "pages/contact/contact.html")

def contact_list(request):
    return render(request, "pages/contact/contact-list.html")

def contact_detail(request):
    return render(request, "pages/contact/contact-detail.html")

def login(request):
    return render(request, "pages/user/login.html")


def forgot_id(request):
    # 확인이 되면 render(request, 'pages/user/forgot-id-result.html') 로 이동!
    return render(request, "pages/user/forgot-id.html")


def forgot_pw(request):
    # 확인이 되면 render(request, 'pages/user/reset-pw.html') 로 이동!
    return render(request, "pages/user/forgot-password.html")


def signup(request):
    return render(request, "pages/user/signup.html")


def post_form(request):
    return render(request, "pages/user/post-form.html")


def support(request):
    return render(request, "pages/admin/support.html")


def about_us(request):
    return render(request, "pages/community/aboutus.html")


def news_list(request):
    return render(request, "pages/community/news-list.html")


def news_detail(request):
    return render(request, "pages/community/news-detail.html")


def user_profile(request):
    return render(request, "pages/user/user-profile.html")


def admin_profile(request):
    return render(request, "pages/admin/admin-profile.html")


def contact_list(request):
    return render(request, "pages/contact/contact-list.html")


def contact_detail(request):
    return render(request, "pages/contact/contact-detail.html")

def fog_result(request):
    return render(request, "pages/user/fog-result.html")



# ========================== 아래는 페이지 확인 차 만든 것임. 삭제해도 됨! ===============================
def forgot_id_result(request):
    return render(request, "pages/user/forgot-id-result.html")

def reset_pw(request):
    # 성공하면 fog.html로 redirect
    return render(request, "pages/user/reset-pw.html")