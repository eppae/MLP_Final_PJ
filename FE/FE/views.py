from django.shortcuts import render, redirect
#---회원관련---
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.utils import timezone
from .models import UploadedFile
# --- fog 관련 ---
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os

def home(request):
    return render(request, "pages/home.html")


def community(request):
    return render(request, "pages/community/community.html")


def contact(request):
    return render(request, "pages/contact/contact.html")


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

# --- 회원관련 views ---
def user_logout(request):
    auth_logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) 
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'pages/user/signup.html', {'form': form})

def user_login(request):
    remembered_username = request.COOKIES.get('remembered_username')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            response = redirect('home')

            if 'remember_username' in request.POST:
                response.set_cookie('remembered_username', username, max_age=30*24*60*60) 
            else:
                response.delete_cookie('remembered_username')

            return response
        else:
            
            if User.objects.filter(username=username).exists():
                error_message = '비밀번호가 올바르지 않습니다.'
            else:
                error_message = '존재하지 않는 ID입니다.'

            return render(request, 'pages/user/login.html', {'error': error_message, 'remembered_username': remembered_username})
        
    else:
        return render(request, 'pages/user/login.html', {'remembered_username': remembered_username})

def forgot_id_result(request):
    return render(request, 'pages/user/forgot-id-result.html')

def forgot_id(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            return render(request, 'pages/user/forgot-id-result.html', {'username': user.username})
        except User.DoesNotExist:
            return render(request, 'pages/user/forgot-id.html', {'error': '해당 이메일로 등록된 아이디가 없습니다.'})

    return render(request, 'pages/user/forgot-id.html')

    # 사용자 검증과 비밀번호 재설정 함수
def check_user_and_reset_password(request, user, new_password):
    form = SetPasswordForm(user, {'new_password1': new_password, 'new_password2': new_password})
    if form.is_valid():
        form.save()
        auth_logout(request)
        user = authenticate(request, username=user.username, password=new_password)
        if user:
            auth_login(request, user)
            messages.success(request, f"비밀번호가 성공적으로 변경되었습니다. 다시 로그인해주세요.")
            return redirect('home')
        else:
            messages.error(request, f"비밀번호 변경 후 로그인 중 오류가 발생했습니다.")
            return redirect('user_login')
    else:
        messages.error(request, f"비밀번호 변경 중 오류가 발생했습니다.")
        return redirect('forgot_pw')

# 사용자 검증 함수
def check_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user = User.objects.get(username=username, email=email)
            return render(request, 'pages/user/forgot-password.html', {'password_found': True, 'user': user})
        except User.DoesNotExist:
            messages.error(request, f"해당 이름 또는 이메일로 된 사용자가 없습니다.")
    return render(request, 'pages/user/forgot-password.html', {'password_found': False})

# 비밀번호 재설정 뷰
def forgot_pw(request):
    if request.method == "POST" and request.POST.get('new_password'):
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user = User.objects.get(username=username, email=email)
            new_password = request.POST.get('new_password')
            return check_user_and_reset_password(request, user, new_password)
        except User.DoesNotExist:
            return render(request, 'pages/user/forgot-password.html', {'error': '잘못입력하셨습니다.'})
    elif request.method == "POST":
        return check_user(request)
    return render(request, 'pages/user/forgot-password.html', {'password_found': False})
    
def get_today_visitors():
    today = timezone.now().date()
    return User.objects.filter(last_login__date=today).count()

def get_daily_users():
    today = timezone.now().date()
    
    daily_users = UploadedFile.objects.filter(upload_date__date=today).count()
    
    return daily_users

def my_stats_view(request):
    daily_visitors = get_today_visitors()
    daily_users = get_daily_users()
    
    context = {
        'daily_visitors': daily_visitors,
        # 'daily_reviews': 문의학기 만들어지면 추가 예정
        'daily_users': daily_users # 파일 처리 완성되면 손봐야함
    }
    return render(request, 'pages/admin/admin-profile.html', context)

# --- fog 관련 ---
def fog(request):
    return render(request, 'pages/test/fog.html')

def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['myfile']
        
        if uploaded_file:
            fs = FileSystemStorage(location='before_fog')
            filename = fs.save(uploaded_file.name, uploaded_file)
            
            # 파일 업로드 정보를 데이터베이스에 저장
            UploadedFile.objects.create(file=filename)
            
            file_url = fs.url(filename)
            
            return HttpResponse(f"파일이 성공적으로 처리됨: {file_url}")
        else:
            return HttpResponse("파일이 처리되지 않음")
            
    return HttpResponse("처리 실패")


# def process_file(request):
    # 파일을 처리 > after_fog에 저장 > 웹페이지에 표출 구현 예정