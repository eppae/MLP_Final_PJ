const button = document.querySelector('#reply-btn');
const collapseElement = document.querySelector('#reply-form-content');

// Add a click event listener to the button
button.addEventListener('click', function () {
    collapseElement.classList.toggle('show');
});

// [E1. 일반 접속자가 댓글, 좋아요/싫어요를 남기려 할 경우]
// 1. ‘로그인이 필요한 서비스입니다.’ 라는 에러 메시지 출력


// [E1. 사용자의 경우, 이미 남긴 공감과는 반대되는 버튼을 누른 경우]
// 1. 기존에 남겼던 공감 버튼을 취소하고 새로 누른 공감 버튼으로 카운팅 한다.

