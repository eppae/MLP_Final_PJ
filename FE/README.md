# BE
### BE의 전반적인 내용은 주로 주석으로 처리해놨습니다!

- base.html
  - **67줄** : user가 관리자일때, 아닐때 조건문 추가 필요(BE)

1. pages/admin
   - admin-profile.html
     - 주석 참고

   - support.html
     - carousel 안의 이미지
     - for문을 통한 내용 반복

2. pages/community
   - aboutus.html
     - profile image
     - introduce(소개)

   - community.html
     - 최근 News, news link

   - news-detail.html
     - post의 타이틀, 작성자, 날짜, 카테고리, edit, delete, content, 댓글개수, 좋아요 및 싫어요
     - 대댓글 작성자, 날짜, 내용

   - news-list.html
     - for문으로 기사 반복
     - pagination


3. contact
   - contact-detail.html
     - 작성자 정보, contact 내용

   - contact-list.html
     - for문 통해서 contact 반복
     - pagination

   - contact.html
     - contact 작성 후 db 저장


4. test
   - fog.html
     - 결과 영상/사진
     - 결과 설명
  
5. user
**forgot 시리즈 + reset_pw 는 FE 폴더의 url, views.py도 참고해주세요**

- forgot-id-result.html
  - 유저의 id 결과

- forgot-id.html
  - email 입력 받아 Id 찾을 수 있도록

- forgot-password.html
  - 비번 리셋을 위해 id, email 입력

- login.html
  - id,pw 입력
  - remember me 추가하긴 했으나 필요없으면 지워도 됨!


- post-form.html
  - 주석 참고

- reset-pw.html
  - 비밀번호 리셋 폼

- signup.html
  - 회원가입 폼. 주석 참고

- user-profile.html
  - 유저 프로필
  - 유저의 테스트 결과 이미지
  - pagination




# FE

더 세부적으로 해야할 것
1. post의 댓글, 대댓글 작성 폼
2. 디자인(three.js / 스크롤 fade out 효과 이용..?)


