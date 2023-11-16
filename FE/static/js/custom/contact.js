const forms = document.querySelectorAll('.validated_form');
const inputs = document.querySelectorAll('input');
const textarea = document.querySelectorAll('textarea');

const checkValidity = () => {
    Array.from(forms).forEach(form => {
        const emailInput = form.querySelector('input[type="email"]');
        const messageTextarea = form.querySelector('textarea');
        const emailErrorMsg = form.querySelector('.valid-email-form');

        // Check email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (emailInput && !emailRegex.test(emailInput.value)) {
            emailErrorMsg.style.display = 'block';
        } else {
            emailErrorMsg.style.display = 'none';
        }

        // Check message length
        const minLength = 1;
        const maxLength = 500;
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

// Call checkValidity when the input or textarea values change
Array.from(inputs).forEach(input => {
    input.addEventListener('input', checkValidity);
});

Array.from(textarea).forEach(ta => {
    ta.addEventListener('input', checkValidity);
});

// Call checkValidity when the page loads
window.addEventListener('load', checkValidity);

