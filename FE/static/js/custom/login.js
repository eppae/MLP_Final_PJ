const forms = document.querySelectorAll('.validated_form');
const inputs = document.querySelectorAll('input')
const errorMessageId = document.querySelector('.valid-id');
const errorMessagePW = document.querySelector('.valid-pw');
const submitBtn = document.querySelector('input[type="submit"]')


const validationId = () =>{
    submitBtn.addEventListener('click',()=>{
        // if (없는 아이디) {
            // errorMessageId.textContent = '등록되지 않은 사용자입니다.';
        //} else {
            // errorMessageId.textContent = '';
        //}
    })
}

const validatonPw = () =>{
    submitBtn.addEventListener('click',()=>{
        // if (맞지 않는 비밀번호) {
            // errorMessageId.textContent = '비밀번호가 맞지 않습니다. 다시 입력해주세요.';
        //} else {
            // errorMessageId.textContent = '';
        //}
    })
}

Array.from(inputs).forEach(input => {
    input.addEventListener('input', validateID);
    input.addEventListener('input', checkDuplicateID);
});

window.addEventListener('load', validateID);
