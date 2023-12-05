import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import Profile


# ---회원 관련 ---

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_message', 'git_address', 'profile_picture']
        
    def __init__(self, *args, **kwargs):           
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        # 프로필 메시지 CSS 수정은 이곳에서!
        self.fields['profile_message'].widget.attrs.update({'class': 'form-control form-control-user'})
        

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='이메일', widget=forms.EmailInput(attrs={'class': 'form-control form-control-user', 'placeholder': '이메일 주소'}))
    terms_agreed = forms.BooleanField(required=True, label='개인정보처리방침 및 이용약관 동의')
    
    class Meta:
        model = User
        fields = ("last_name", "username", "password1", "password2", "email")
        labels = {
            'last_name' : '이름',
            'username' : 'ID',
            # 'password1' : '비밀번호',         password
            # 'password2' : '비밀번호 확인',    password confirmation   
            # 이렇게 나와서 __init__에 수정하기로함 이유는 모르겠지만 비밀번호만 그러는걸 보면 보안문제?
            # >> 보안문제 X / 상속받아 폼을 사용할 때 메타 클래스에서 속성을 덮으려 할 때 문제 발생
            # 다른 내장 폼의 기본 동작을 오버라이드하고자 할 때는 
            # __init__ 메서드 내에서 필드의 레이블을 직접 설정하는 것이 가장 확실한 방법!!!
        }
        error_messages = {  # 오류메시지가 영어로 나와서 직접 설정해줌
            'username': {
                'unique': _("이미 존재하는 사용자명입니다."),
                'required': _("사용자명을 입력하세요."),
            },
            'last_name': {
                'required': _("이름을 입력하세요."),  
            },
        }    

    def clean_username(self):       # ID 유효성 검사 및 에러메시지 추가(기본제공하지만 영어로만 제공해줘서 추가함)
        username = self.cleaned_data['username']
        # if not username.isalpha():        # 영어만 걸러줘서 지움
        if not re.match(r'^[a-zA-Z0-9]*$', username):       #영어 숫자
            raise ValidationError(_("ID는 영어만 가능합니다"))
        if len(username) > 10:
            raise ValidationError(_("ID를 10자 이하로 작성하셔요."))
        return username
        
    def __init__(self, *args, **kwargs):           
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
        # 회원가입 CSS는 이곳에서!!
        self.fields['last_name'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': '이름'})
        self.fields['username'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': '사용자 ID'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': '비밀번호'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control form-control-user', 'placeholder': '비밀번호 확인'})
        
        
        self.fields['password1'].label = '비밀번호'
        self.fields['password2'].label = '비밀번호 확인'  
        
        self.fields['last_name'].widget.attrs.update({
            'title': '이름을 입력하시오'
        })        
        self.fields['username'].widget.attrs.update({
            'title': 'ID를 입력하시오'
        })        
        self.fields['password1'].widget.attrs.update({
            'pattern': '^(?=.*[A-Za-z])(?=.*\\d).{8,}$',
            'title': '비밀번호는 최소 8자 이상\n대문자, 소문자, 숫자를 각각 최소 한 개 이상 포함해야 합니다.'
        })
        self.fields['password2'].widget.attrs.update({
            'title': '위와 동일하게 입력하세요.'
        })
        self.fields['email'].widget.attrs.update({
            'title': '이메일 형식에 맞추시오'
        })    
        
        
    def save(self, commit=True):        # 내가 넣은 field와 UserCreationForm의 field 유효성 검사 후 저장
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
class CommentForm(forms.Form):
    comment_message = forms.CharField(widget=forms.Textarea)
    parent_id = forms.IntegerField(required=False, widget=forms.HiddenInput)