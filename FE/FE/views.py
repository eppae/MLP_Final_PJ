#---안개관련---
from django.core.paginator import Paginator
from django.db.models import Q
from .models import ContactMessage
from django.shortcuts import render, redirect , get_object_or_404
#---회원관련---
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.utils import timezone
from .models import Profile, UploadedFile
from .forms import ProfileForm
# --- fog 관련 ---
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import dehazing
from finalProject.ml_utils.inference import inference, FLAGS
import os

def home(request):
    return render(request, "pages/home.html")


def community(request):
    return render(request, "pages/community/community.html")

def contact(request):
    return render(request, "pages/contact/contact.html")

def contact_list(request):
    return render(request, "pages/contact/contact-list.html")

def contact_detail(request):
    return render(request, "pages/contact/contact-detail.html")


def post_form(request):
    return render(request, "pages/user/post-form.html")

def support(request):
    return render(request, "pages/admin/support.html")

def review_detail(request):
    return render(request, "pages/user/review-detail.html")


def news_list(request):
    return render(request, "pages/community/news-list.html")

def news_detail(request):
    return render(request, "pages/community/news-detail.html")

def contact_list(request):
    page_number = request.GET.get('page','1')
    print("Page number:", page_number)
    contact_messages = ContactMessage.objects.all()
    print("Contact Messages:", contact_messages)
    kw = request.GET.get('contact_kw','') # 검색어
    if kw:
        contact_messages = contact_messages.filter(
            Q(title__icontains=kw) |  # 제목 검색
            Q(message__icontains=kw) |  # 내용 검색
            Q(email__icontains=kw)  # 이메일 검색
        ).distinct()
    paginator = Paginator(contact_messages, 10)
    page_obj = paginator.get_page(page_number)
    context = {'recent_page':page_obj,'page':page_number,'contact_messages':contact_messages, 'kw':kw}
    return render(request, "pages/contact/contact-list.html",context)


def contact_detail(request, post_num):
    contact_message = get_object_or_404(ContactMessage, post_num=post_num)

    return render(request, "pages/contact/contact-detail.html",{'contact_message':contact_message})


def submit_contact(request):
    page_number = request.GET.get('page','1')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        title = request.POST.get('title')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contact_message = ContactMessage(
            first_name = first_name,
            last_name = last_name,
            title = title,
            email = email,
            message = message
        )
        contact_message.save()
        print(contact_message)
        return render(request, 'pages/contact/contact.html', {'contact_message': contact_message})

    return HttpResponse("Invalid Request Method")

def delete_contact(request):
    if request.method == 'POST':
        selected_contacts = request.POST.getlist('selected_boxes')
        ContactMessage.objects.filter(post_num__in=selected_contacts).delete()
    return render(request,'pages/contact/contact_list.html')

# ========================== 에러 페이지 ===============================

def page_not_found(request, exception):
    print("page_not_found function is called!")  # 디버깅용 메시지
    return render(request, 'pages/error/404.html', status=404)


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



def user_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=request.user.profile)

    context = {
        'form': form,
    }
    return render(request, 'pages/user/user-profile.html', context)


def admin_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=request.user.profile)

    context = {
        'form': form,
    }
    return render(request, 'pages/admin/admin-profile.html', context)


def about_us(request):
    profiles = []

    # 민제님 프로필 조회
    try:
        user_a = User.objects.get(last_name="김민제", username="mj1")
        profiles.append(Profile.objects.get(user=user_a))
    except (User.DoesNotExist, Profile.DoesNotExist):
        pass 

    # 수현님 프로필 조회
    try:
        user_b = User.objects.get(last_name="강수현", username="sh1")
        profiles.append(Profile.objects.get(user=user_b))
    except (User.DoesNotExist, Profile.DoesNotExist):
        pass  

    # 동엽님 프로필 조회
    try:
        user_b = User.objects.get(last_name="이동엽", username="dy1")
        profiles.append(Profile.objects.get(user=user_b))
    except (User.DoesNotExist, Profile.DoesNotExist):
        pass

    # 우림님 프로필 조회
    try:
        user_b = User.objects.get(last_name="장우림", username="wl1")  
        profiles.append(Profile.objects.get(user=user_b))
    except (User.DoesNotExist, Profile.DoesNotExist):
        pass

    # 홍태광 프로필 조회
    try:
        user_htk96 = User.objects.get(last_name="홍태광", username="htk96")
        profiles.append(Profile.objects.get(user=user_htk96))
    except (User.DoesNotExist, Profile.DoesNotExist):
        pass

    context = {
        'profiles': profiles,
    }
    return render(request, 'pages/community/aboutus.html', context)

    
def get_today_visitors():
    today = timezone.now().date()
    return User.objects.filter(last_login__date=today).count()

def get_daily_users():
    today = timezone.now().date()
    
    daily_users = UploadedFile.objects.filter(upload_date__date=today).count()
    
    return daily_users

#json파일에 한줄씩///

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
    context = {}

    if request.method == 'POST' and request.FILES.get('image'):
        # 이미지 파일 저장
        image_file = request.FILES['image']
        fs = FileSystemStorage(location='before_fog/')
        filename = fs.save(image_file.name, image_file)
        uploaded_file_url = fs.url(filename)

        # 데이터베이스에 이미지 정보 저장
        new_image = dehazing(original_image=filename)
        new_image.save()

        # inference 설정
        input_file_path = os.path.join(fs.location, filename)
        output_file_path = os.path.join('after_fog', 'processed_' + filename)
        FLAGS.model = 'finalProject/ml_models/Hazy_to_Clear.pb'
        FLAGS.input_file = input_file_path  # 단일 파일 경로 설정
        FLAGS.output_file = output_file_path  # 결과 파일 경로 설정
        
        # AI 모델을 사용하여 이미지 처리
        model_path = 'finalProject/ml_models/Hazy_to_Clear.pb'
        image_size = 256
        inference(input_file_path, output_file_path, model_path, image_size)

        # 처리된 이미지의 URL
        processed_file_url = '/after_fog/processed_' + filename

        # 데이터베이스에 처리된 이미지 정보 업데이트
        new_image.processed_image = 'processed_' + filename
        new_image.save()

        context = {
            'uploaded_file_url': uploaded_file_url,
            'processed_file_url': processed_file_url
        }

    return render(request, 'pages/test/fog.html', context)


def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['myfile']
        
        if uploaded_file:
            fs = FileSystemStorage(location='before_fog')
            filename = fs.save(uploaded_file.name, uploaded_file)
            
            UploadedFile.objects.create(file=filename)
            
            file_url = fs.url(filename)
            
            return HttpResponse(f"파일이 성공적으로 처리됨: {file_url}")
        else:
            return HttpResponse("파일이 처리되지 않음")
            
    return HttpResponse("처리 실패")


# def process_file(request):
    # 파일을 처리 > after_fog에 저장 > 웹페이지에 표출 구현 예정
    
# --- 민제님 views ---