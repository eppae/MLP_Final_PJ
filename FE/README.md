# BE
### BE의 전반적인 내용은 주로 주석으로 처리해놨습니다!
### news-list, news-detail 부분 추가사항 있습니다!
---
### to. BE
##### 11.23
1. Our Product에서 제 컴퓨터에는 파일 업로드 표시가 안되는데, 일단 css랑 레이아웃 수정했습니다. 확인부탁드려요

---
### to. BE
##### 11.16~
1. OUR PRODUCT : Process버튼은 어떤건가용..?
  - A: UPLOAD로 파일이 올라가지면 "PROCESS!" 버튼이 나타납니당
2. signup.html에서 checkbox가 두 개 나옵니다! label은 체크가 안되는데 확인해주세요
  - A: BE에선 고쳤었는데 프로젝트 옮기면서 또 생겼나보네요 확인하겠습니다!
##### 11.17~
 

---
### to. FE
>> 작업은 지난주에 완료됐는데 이번주에 뻘짓을 하느라 늦게 올려드립니다 FE코드도 건드려서 죄송합니다ㅠ
##### 11.16~
1. login, sigup ID/PW찾기 나눠놨습니다
2. sigup에서 에러메시지 표시도 같이하려고 양식은 동일하게 form 태그로 수정
3. base에 logout 추가(admin과 user구분했습니다)
4. OUR PRODUCT에 "PEOCESS!" 버튼 추가(일단 디렉토리에 업로드된 파일 저장만)
5. ~~프로필 수정부분은 어떻게 하는게 좋을지~~
##### 11.28~
6. staff 계정에 수현님이 정하신 이모지로 수정해놨습니다./사용자 입장의 처리 후 사진 볼 ID도 밑에 적어놨습니다.
  - 민재님= 이름: 김민제 / ID: mj1 / PW: 1q2w3e4rQ
  - 수현님= 이름: 강수현 / ID: sh1 / PW: 1q2w3e4rQ
  - 동엽님= 이름: 이동엽 / ID: dy1 / PW: 1q2w3e4rQ
  - 우림님= 이름: 장우림 / ID: wl1 / PW: 1q2w3e4rQ
  - 홍태광= 이름: 홍태광 / ID: tk1 / PW: 1q2w3e4rQ
  
  - 사용자= 이름: 예시용 / ID: ex1 / PW: 1q2w3e4rQ
  ---

7. fog 수정을 위해 결정해야 할 부분(1과 2로 나뉨)
    1. upload 누르자마자 progressbar가 나옴 > (파일 선택 후 생기는)Process 누르면 나오도록 수정.<br>
    2. progressbar를 없애고 Process 버튼을 누르면 경과시간만 나오도록 바꿈.
      > 시간 경과로 바꾸기엔 js코드가 너무 엄청나서 고민이됩니다,,<br>
      > (저번에 작성하느라 고생하신 걸로 알고있는데..)<br>
      > 아무튼 작성하신분이 남길지 바꿀지 정해주시거나 의견 나눠서 결정하게되면 맞게 수정할게요!
8. ABOUTUS에 민제님 소개창만 위치가 4명보다 좀 위에 나오는데 (손보는게 낫겠죠..?)
  > 민제님 review 부분 완성되면 통계 추가할 때 같이 수정하겠습니다

9. admin profile / user profile부분 만들다보니 영어, 한글 짬뽕이 되었는데 통일하는게 좋을듯합니다 FE분들의 고견이 필요합니다

---

### BE 수정 필!
1. ~~admin 통계, ~~login의 Remember Me~~ : 프로젝트 여러번 옮기면서 오류났는데 안잡히네요,, 수정 예정...~~
2. ~~모델 나오면 OUR PRODUCT에 파일처리, after저장, 표출 추가해야함~~
3. ~~프사 넣기~~



### 예외사항 
- static/js/custom/signup.js
  - BE와 연동할 필요가 있어서 남겨뒀습니다! => 중복되는 Id가 있을 경우

- static/js/custom/login.js
- forgot~ 예외사항. => 드라이브의 FE 폴더 내, 예외사항 문서 참고

### FE template에서 필요한 부분

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
     - **수정 및 삭제는 admin 혹은 작성자 본인만 가능하도록 해야함**
     - **대댓글 폼은 첫번째 댓글의 reply에 적용되어 있습니다! 해당 폼 참고해서 작성해주시면 됩니다!**

   - news-list.html
     - for문으로 기사 반복
     - pagination
     - **작성하기 버튼은 admin만 보이도록 할 필요가 있음**


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

- review-detail.html
  - news-detail.html과  `community.writer` 같은 부분을 제외하고 똑같음!


# FE

더 세부적으로 해야할 것
1. 디자인(three.js / 스크롤 fade out 효과 이용..?)