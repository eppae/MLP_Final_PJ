#---안개관련---
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
from .models import ContactMessage,PostForm
from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse
from .models import dehazing
from finalProject.ml_utils.inference import inference
from django.core.files.base import ContentFile
import os
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
#---회원관련---
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.utils import timezone
from datetime import datetime
from .models import Profile
from .forms import ProfileForm
from django.forms.models import modelform_factory
#--- comment ---
from .models import Comment
from .forms import CommentForm
from django.urls import reverse
from django.http import HttpResponseRedirect
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

@login_required
def post_form(request):
    current_time = datetime.now()
    context = {
        'current_user':request.user,
        'current_time':current_time,
    }
    return render(request, "pages/user/post-form.html",context)

def support(request, n_category=None):
    post_per_page = 5
    newsposts = PostForm.objects.exclude(category='news')
    if n_category:
        newsposts = PostForm.objects.filter(category=n_category)
    #pagenator 객체 생성
    pagenator = Paginator(newsposts,post_per_page)
    #현재 페이지 번호 가져오기
    page = request.GET.get('page',1)
    #print(page)
    try:
        newsposts = pagenator.page(page)
    except (PageNotAnInteger,EmptyPage):
        newsposts = pagenator.page(1)

    context = {'newsposts': newsposts}
    #print(newsposts.paginator.num_pages)
    #print(newsposts.has_previous)
    #print(newsposts.has_next)
    return render(request, "pages/admin/support.html", context)

def delete_post(request,pk):
    post = get_object_or_404(PostForm, post_num=pk)
    post.delete()
    return redirect('support')

def edit_post(request,pk):
    newspost = get_object_or_404(PostForm, post_num=pk)
    return render(request, "pages/user/edit-post-form.html",newspost)

def review_detail(request):
    return render(request, "pages/user/review-detail.html")

def edit_post_view(request,pk):
    current_user = request.user
    current_time = datetime.now()
    newspost = get_object_or_404(PostForm, post_num=pk)
    initial_data = {
        'SelectCategory':newspost.category,
        'title': newspost.title,
        'text':newspost.text,
    }
    context = {'newspost':newspost,'form_initial':initial_data,'current_user':current_user,'current_time':current_time}
    print(initial_data)
    return render(request, "pages/user/edit-post-form.html",context)

def edit_post_text(request, pk):
    current_user = request.user
    current_time = datetime.now()
    newspost = get_object_or_404(PostForm, post_num=pk)

    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        category = request.POST.get('SelectCategory')
        img = request.FILES.get('img')

        newspost.title = title
        newspost.text = text
        newspost.category = category
        if img:
            newspost.img = img

        newspost.save()

        return redirect('news_detail', post_num=newspost.post_num)

    context = {
        'newspost': newspost,
        'current_user': current_user,
        'current_time': current_time
    }

    return render(request, "pages/user/edit-post-form.html", context)

def news_list(request,n_category=None):
    newsposts = PostForm.objects.filter(category='news')
    if n_category:
        newsposts = PostForm.objects.filter(category=n_category)
    print(newsposts)
    context = {'newsposts':newsposts}
    return render(request, "pages/community/news-list.html", context)

def n_category_news_list(request,n_category):
    return support(request,n_category=n_category)

def news_detail(request,post_num):
    writer = request.user
    current_time = datetime.now()
    print("post_num:", post_num)
    newspost = get_object_or_404(PostForm,post_num=post_num)
    comments = Comment.objects.filter(post=newspost)
    print(comments)
    context = {'newspost':newspost,'writer':writer,'current_time':current_time,'comments':comments}
    return render(request, "pages/community/news-detail.html", context)

def like_newspost(request, pk):
    newspost = get_object_or_404(PostForm, post_num=pk)
    liked = False
    if newspost.likes.filter(id=request.user.id).exists():
        newspost.likes.remove(request.user)
        liked = False
    else:
        newspost.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('news_detail', args=[str(pk)]))

def dislike_newspost(request, pk):
    newspost = get_object_or_404(PostForm, post_num=pk)
    disliked = False
    if newspost.dislikes.filter(id=request.user.id).exists():
        newspost.dislikes.remove(request.user)
        disliked = False
    else:
        newspost.dislikes.add(request.user)
        disliked = True
    return HttpResponseRedirect(reverse('news_detail', args=[str(pk)]))

def create_post(request):
    if request.method =='POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        category = request.POST.get('SelectCategory')
        img = request.FILES.get('img')
        writer = request.user
        Post = PostForm(
            title = title,
            text = text,
            category = category,
            img = img,
            writer = writer,
        )
        Post.save()
        print(Post)
        if category == 'news':
            return redirect('news_list')
        else:
            return redirect('support')
    return HttpResponse("Invalid Request Method")

@login_required()
def create_comment(request, post_num):
    post = get_object_or_404(PostForm, post_num=post_num)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            writer = request.user
            content = form.cleaned_data['comment_message']
            parent_id = form.cleaned_data.get('parent_id', None)

            is_reply = False
            if parent_id:
                parent_comment = get_object_or_404(Comment, pk=parent_id)
                is_reply = True
                comment = Comment(
                    writer=writer,
                    content=content,
                    post=post,
                    parentcomment=parent_comment,
                    is_reply = is_reply,
                )
            else:
                comment = Comment(
                    writer=writer,
                    content=content,
                    post=post,
                    is_reply=is_reply,
                )

            comment.save()

    comments = Comment.objects.filter(post=post)

    # Redirect to the news_detail view for the same post_num
    return redirect('news_detail', post_num=post_num)

def delete_comment(request,post_num,comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    # Check if the user has permission to delete the comment (optional)
    if request.user == comment.writer:
        comment.delete()

    return redirect('news_detail', post_num=post_num)

def contact_list(request,category=None):
    page_number = request.GET.get('page','1')
    print("Page number:", page_number)
    contact_messages = ContactMessage.objects.all()
    print("Contact Messages:", contact_messages)
    kw = request.GET.get('contact_kw','') # 검색어

    if category:
        contact_messages = contact_messages.filter(category=category)

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

def contact_list_category(request,category):
    return contact_list(request, category=category)
def contact_detail(request, post_num):
    contact_message = get_object_or_404(ContactMessage, post_num=post_num)

    return render(request, "pages/contact/contact-detail.html",{'contact_message':contact_message})
    return contact_list(request, category=category)


def support_detail(request, post_num):
    support_message = get_object_or_404(PostForm, post_num=post_num)

    return render(request, "pages/contact/contact-detail.html",{'contact_message':support_message})


def submit_contact(request):
    page_number = request.GET.get('page','1')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        title = request.POST.get('title')
        email = request.POST.get('email')
        message = request.POST.get('message')
        category = request.POST.get('category')

        contact_message = ContactMessage(
            first_name = first_name,
            last_name = last_name,
            title = title,
            email = email,
            category = category,
            message = message,

        )
        contact_message.save()
        print(contact_message)
        return render(request, 'pages/contact/contact.html', {'contact_message': contact_message})

    return HttpResponse("Invalid Request Method")

def delete_contact(request):
    if request.method == 'POST':
        selected_contacts = request.POST.getlist('selected_boxes')
        ContactMessage.objects.filter(post_num__in=selected_contacts).delete()
    return render(request,'pages/contact/contact-list.html')

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


# --- 프로필 변경 ---profile model을 찢어놓음
ProfilePictureForm = modelform_factory(Profile, fields=('profile_picture',))
ProfileInfoForm = modelform_factory(Profile, fields=('profile_message', 'git_address',))


@login_required
def user_profile(request):
    profile_picture_form = ProfilePictureForm(request.POST or None, request.FILES or None, instance=request.user.profile)
    profile_info_form = ProfileInfoForm(request.POST or None, instance=request.user.profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=request.user.profile)
        
    if request.method == 'POST':
        # 프사 업데이트 폼 처리
        if 'profile_picture' in request.FILES:
            if profile_picture_form.is_valid():
                profile_picture_form.save()
                messages.success(request, '프로필 사진이 성공적으로 업데이트되었습니다.')
                return redirect('user_profile')
        # 메시지 수정 폼 처리
        if profile_info_form.is_valid():
            profile_info_form.save()
            messages.success(request, '프로필 정보가 성공적으로 업데이트되었습니다.')
            return redirect('user_profile')

    # 페이지당 4개로 처리한 이미지 넣기
    user_dehazing_images = dehazing.objects.filter(user=request.user)
    total_images = user_dehazing_images.count()
    
    paginator = Paginator(user_dehazing_images, 2) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'profile_picture_form': profile_picture_form,
        'profile_info_form': profile_info_form,
        'profile': request.user.profile,
        
        'form': form,
        'page_obj': page_obj,
        'total_images': total_images,
    }
    return render(request, 'pages/user/user-profile.html', context)


def admin_profile(request):
    # ProfileForm에서 profile_picture 필드만 사용하는 새로운 폼 클래스를 생성
    profile_picture_form = ProfilePictureForm(request.POST or None, request.FILES or None, instance=request.user.profile)
    profile_info_form = ProfileInfoForm(request.POST or None, instance=request.user.profile)
    
    #통계 context 넣기
    daily_visitors = get_daily_visitors()
    daily_contacts = get_daily_contacts()
    total_contacts = get_total_contacts()
    daily_reviews = get_daily_reviews()
    total_reviews = get_total_reviews()
    daily_users = get_daily_users()
    total_users = get_total_users()

    if request.method == 'POST':
        # 프사 업데이트 폼 처리
        if 'profile_picture' in request.FILES:
            if profile_picture_form.is_valid():
                profile_picture_form.save()
                messages.success(request, '프로필 사진이 성공적으로 업데이트되었습니다.')
                return redirect('admin_profile')
        # 메시지 수정 폼 처리
        if profile_info_form.is_valid():
            profile_info_form.save()
            messages.success(request, '프로필 정보가 성공적으로 업데이트되었습니다.')
            return redirect('admin_profile')
        
    # contacts 모아보기
    recent_contacts=ContactMessage.objects.all().order_by('-created_at')[:2]
    # news 모아보기
    recent_news = PostForm.objects.filter(category='news').order_by('-created_at')[:2]
    # support 모아보기
    recent_supports = PostForm.objects.exclude(category='news').order_by('-created_at')[:2]

    context = {
        'profile_picture_form': profile_picture_form,
        'profile_info_form': profile_info_form,
        'profile': request.user.profile,
        # ▼통계 context
        'daily_visitors': daily_visitors,
        'daily_contacts': daily_contacts,
        'total_contacts': total_contacts,
        'daily_reviews': daily_reviews,
        'total_reviews': total_reviews,
        'daily_users': daily_users,
        'total_users': total_users,
        'recent_contacts': recent_contacts,
        'recent_news': recent_news,
        'recent_supports':recent_supports, #오타 있었음, 이젠 url 수정 필요
    }
    
    return render(request, 'pages/admin/admin-profile.html', context)
    
    
def get_daily_visitors():   # 방문자 수
    today = timezone.now().date()
    daily_visitors = User.objects.filter(last_login__date=today).count()
    
    return daily_visitors


def get_daily_contacts():
    today = timezone.now().date()
    daily_contacts = ContactMessage.objects.filter(created_at__date=today).count()
    
    return daily_contacts


def get_total_contacts():
    total_contacts = ContactMessage.objects.all().count()
    
    return total_contacts


def get_daily_reviews():
    today = timezone.now().date()
    daily_reviews = Comment.objects.filter(created_at__date=today).count()
    
    return daily_reviews

def get_total_reviews():
    total_reviews = Comment.objects.all().count()
    
    return total_reviews
    
    
def get_total_users():
    total_users = dehazing.objects.all().count()
    
    return total_users


def get_daily_users():
    today = timezone.now().date()
    daily_users = dehazing.objects.filter(uploaded_at__date=today).count()
    
    return daily_users
    
    
   
    
def about_us(request):
    profiles = []

    # 민제님 프로필 조회
    try:
        staff = User.objects.get(last_name="김민제", username="mj1")
        profiles.append(Profile.objects.get(user=staff))
    except (User.DoesNotExist, Profile.DoesNotExist):
        pass 

    # 수현님 프로필 조회
    try:
        staff = User.objects.get(last_name="강수현", username="sh1")
        profiles.append(Profile.objects.get(user=staff))
    except (User.DoesNotExist, Profile.DoesNotExist):
        pass  

    # 동엽님 프로필 조회
    try:
        staff = User.objects.get(last_name="이동엽", username="dy1")
        profiles.append(Profile.objects.get(user=staff))
    except (User.DoesNotExist, Profile.DoesNotExist):
        pass

    # 우림님 프로필 조회
    try:
        staff = User.objects.get(last_name="장우림", username="wl1")  
        profiles.append(Profile.objects.get(user=staff))
    except (User.DoesNotExist, Profile.DoesNotExist):
        pass

    # 홍태광 프로필 조회
    try:
        staff = User.objects.get(last_name="홍태광", username="tk1")
        profiles.append(Profile.objects.get(user=staff))
    except (User.DoesNotExist, Profile.DoesNotExist):
        pass

    context = {
        'profiles': profiles,
    }
    return render(request, 'pages/community/aboutus.html', context)


# --- fog 관련 ---
progress_status = {}

@login_required
def fog(request):
    context = {}
    
    def update_progress(progress_value):
        progress_status[request.user.id] = progress_value

    if request.method == 'POST' and request.FILES.get('image'):
        # 이미지 파일 저장
        image_file = request.FILES['image']
        new_image = dehazing(user=request.user, original_image=image_file)
        new_image.save()

        # inference 설정 및 이미지 처리
        input_file_path = new_image.original_image.path
        output_file_name = 'processed_' + image_file.name
        output_file_path = os.path.join('media/after_fog/', output_file_name)
        
        # AI 모델을 사용하여 이미지 처리
        model_path = 'finalProject/ml_models/Hazy_to_Clear.pb'
        image_size = 256
        inference(input_file_path, output_file_path, model_path, image_size, update_progress)

        # 처리된 이미지 저장
        new_image.processed_image.save(output_file_name, ContentFile(open(output_file_path, 'rb').read()))
        new_image.save()
        
        
        # 진행상태 초기화
        update_progress(0)

        context = {
            'uploaded_file_url': new_image.original_image.url,
            'processed_file_url': new_image.processed_image.url
        }

    return render(request, 'pages/test/fog.html', context)

def get_progress(request):
    user_id = request.user.id
    progress = progress_status.get(user_id, 0)
    return JsonResponse({'progress': progress})

    