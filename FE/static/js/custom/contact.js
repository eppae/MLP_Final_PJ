// [E1. 잘못된 email 형식]
// 1. ‘이메일 형식이 잘못되었습니다. 다시 입력해주세요’ 라는 에러 메시지 출력
const validationForm = () => {
    const forms = document.querySelectorAll('.validated_form')
    const inputs = document.querySelectorAll('input')
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
    })
}

// [E2. 글자수 초과] ====> 500자
// 2. “허용된 글자수를 초과했습니다.”라는 에러 메시지를 반환

