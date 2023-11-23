document.addEventListener('DOMContentLoaded', function () {

    $(window).scroll(function () {
        const scrollTop = $(this).scrollTop()
        const movement = scrollTop / 0.35
        const blurAmount = Math.min(scrollTop / 20, 10)
        if (scrollTop < window.innerHeight) {
            $('.fog-container-left').css('transform', `translateX(-${movement}px)`)
            $('.fog-container-right').css('transform', `translateX(${movement}px)`)

            $('.fog-container-left, .fog-container-right').addClass('blur')
        } else{
            $('.background').css('display', 'none')
        }
    })
})