// 안개
document.addEventListener("DOMContentLoaded", function () {
  $(window).scroll(function () {
    const scrollTop = $(this).scrollTop();
    const movement = scrollTop / 0.35;
    const blurAmount = Math.min(scrollTop / 20, 10);
    if (scrollTop < window.innerHeight) {
      $(".fog-container-left").css("transform", `translateX(-${movement}px)`);
      $(".fog-container-right").css("transform", `translateX(${movement}px)`);

      $(".fog-container-left, .fog-container-right").addClass("blur");
    } else {
      $(".background").css("display", "none");
    }
  });
});

// 애니메이션
const observer = new IntersectionObserver(callback, { threshold: 0.07 });
const targetElements = document.querySelectorAll(".animation-target");
targetElements.forEach((targetElement) => {
  observer.observe(targetElement);
});

let wasInterseciong = false;

function callback(entries, observer) {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add(
        "animate__animated","animate__slideInUp"
      );
    }
  });
}
