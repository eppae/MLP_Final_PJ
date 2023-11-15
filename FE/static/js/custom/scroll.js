document.addEventListener('DOMContentLoaded', function () {
    window.addEventListener('scroll', function () {
        const footer = document.querySelector('.footer-container');
        let scrollPosition = window.innerHeight + window.scrollY;

        if (scrollPosition >= document.body.offsetHeight - 30) {
            footer.classList.add('show-footer');
        } else {
            footer.classList.remove('show-footer');
        }
    });
});