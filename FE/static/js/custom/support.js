// 대댓글 작성
const buttonForReply = document.querySelector('#reply-btn');
const collapseElement = document.querySelector('#reply-form-content');
buttonForReply.addEventListener('click', function () {
    collapseElement.classList.toggle('show');
});

// textarea
const forms = document.querySelectorAll('.validated_form');
const textarea = document.querySelectorAll('textarea');

const checkValidity = () => {
    Array.from(forms).forEach(form => {
        const messageTextarea = form.querySelector('textarea');
        
        // Check message length
        const minLength = 1;
        const maxLength = 1000;
        const msgInputErrorMsg = form.querySelector('.valid-msg-input');
        const msgLengthErrorMsg = form.querySelector('.valid-msg');

        if(messageTextarea && messageTextarea.value.length < minLength){
            msgInputErrorMsg.style.display = 'block';
        } else{
            msgInputErrorMsg.style.display = 'none';
        }

        if (messageTextarea && messageTextarea.value.length > maxLength) {
            msgLengthErrorMsg.style.display = 'block';
        } else {
            msgLengthErrorMsg.style.display = 'none';
        }
    });
};


Array.from(textarea).forEach(ta => {
    ta.addEventListener('input', checkValidity);
});

// Call checkValidity when the page loads
window.addEventListener('load', checkValidity);

