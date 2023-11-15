const forms = document.querySelectorAll('.validated_form');
const inputs = document.querySelectorAll('input')
const errorMessagePW = document.querySelector('.valid-pw');
const informMessagePW = document.querySelector('.valid-pw-inform');
const errorMessagePWRe = document.querySelector('.valid-pw-repeat');

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


Array.from(inputs).forEach(input => {
    input.addEventListener('input', validatePassword);
    input.addEventListener('input', validateRepeatPassword);
});

window.addEventListener('load', validatePassword);
