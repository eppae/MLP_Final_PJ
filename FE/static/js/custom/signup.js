const forms = document.querySelectorAll('.validated_form');
const inputs = document.querySelectorAll('input')
const errorMessageId = document.querySelector('.valid-id');
const errorMessagePW = document.querySelector('.valid-pw');
const informMessagePW = document.querySelector('.valid-pw-inform');
const errorMessagePWRe = document.querySelector('.valid-pw-repeat');
const errorCheckBox = document.querySelector('.valid-checkbox');
const submitBtn = document.querySelector('input[type="submit"]')

// 예외상황 1
const validateID = function () {
    Array.from(forms).forEach(form => {
        const inputId = form.querySelector('.form-input-id');
        const regex = /^[a-zA-Z0-9]+$/;
        const isValidFormat = regex.test(inputId.value);

        if (inputId.value.length > 10) {
            errorMessageId.textContent = 'ID는 10글자 이하로 작성해 주십시오.';
        } else if (inputId.value.length > 0 && !isValidFormat) {
            errorMessageId.textContent = 'ID는 영어, 숫자로 입력해주십시오.';
        } else {
            errorMessageId.textContent = '';
        }
    });
};

// [E1. ID가 중복되는 경우]
// 1. “사용 불가능한 ID입니다.” 에러메시지 반환
const checkDuplicateID = function () {
    // if (중복되었을 때) {
        // errorMessageId.textContent = '사용 불가능한 ID입니다.';
    //} else {
        // errorMessageId.textContent = '사용 가능한 ID입니다.';
        // errorMessageId.style.color = 'green';
    //}
};

// 예외사항 3
const validatePassword = function () {
    Array.from(forms).forEach(form => {
        const inputPW = form.querySelector('.form-input-pw');
        const regexPW = /^(?=.*[a-zA-Z0-9])(?=.*\d)(?=.*[!@#$%^&*~]).{8,}$/;
        const isValidFormatPW = regexPW.test(inputPW.value);

        if (!isValidFormatPW) {
            errorMessagePW.textContent = '조건에 부합하지 않는 PW입니다.';
        } else {
            errorMessagePW.textContent = '';
            informMessagePW.style.display = 'none';
        }
    });
};

// 예외사항 4
const validateRepeatPassword = function(){
    Array.from(forms).forEach(form =>{
        const inputPW = form.querySelector('.form-input-pw');
        const inputPWRe = form.querySelector('.form-input-pw-re');
        
        if(inputPWRe.value.length >=1 && (inputPW.value !== inputPWRe.value)){
            errorMessagePWRe.textContent = '설정한 비밀번호와 같지 않습니다.';
            errorMessagePWRe.style.display = 'block';     
        } else{
            errorMessagePWRe.textContent = '';        
        }
    });
};

// 예외사항 5
const validateCheckBox = function () {
    Array.from(forms).forEach(form =>{
        const checkbox = form.querySelector('input[type="checkbox"]')

        submitBtn.addEventListener('click',()=>{
            if(!checkbox.checked){
                errorCheckBox.textContent = '개인정보 처리방침에 동의해 주십시오.';
                errorCheckBox.style.display = 'block';
            } else {
                errorCheckBox.textContent = '';
            }
        })
    });
};

Array.from(inputs).forEach(input => {
    input.addEventListener('input', validateID);
    input.addEventListener('input', checkDuplicateID);
    input.addEventListener('input', validatePassword);
    input.addEventListener('input', validateRepeatPassword);
    input.addEventListener('input', validateCheckBox);
});

window.addEventListener('load', validateID);
