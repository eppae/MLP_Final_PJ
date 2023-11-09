from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, "pages/home.html")


def fog(request):
    return render(request, "pages/test/fog.html")


def community(request):
    return render(request, "pages/community/community.html")


def contact(request):
    return render(request, "pages/contact/contact.html")


def login(request):
    return render(request, "pages/user/login.html")


def forgot_pw(request):
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