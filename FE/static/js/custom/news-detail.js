// 대댓글 작성
const button = document.querySelector('#reply-btn');
const collapseElement = document.querySelector('#reply-form-content');
button.addEventListener('click', function () {
    collapseElement.classList.toggle('show');
});

// [E1. 사용자의 경우, 이미 남긴 공감과는 반대되는 버튼을 누른 경우]
// 1. 기존에 남겼던 공감 버튼을 취소하고 새로 누른 공감 버튼으로 카운팅 한다.


// BE -> news-detail, review-detail로 나뉘어진 것 확인!
//https://github.com/Imshyeon/webproject2/tree/main/mysite/blog
//위의 model, views, forms 등 참고..!
