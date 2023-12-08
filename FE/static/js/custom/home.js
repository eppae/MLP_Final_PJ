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
const observer = new IntersectionObserver(callback, { threshold: 0.05 });
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

// image
function initComparisons() {
  var x, i;
  x = document.getElementsByClassName("img-comp-overlay");
  for (i = 0; i < x.length; i++) {
    compareImages(x[i]);
  }
  function compareImages(img) {
    var slider, img, clicked = 0, w, h;
    w = img.offsetWidth;
    h = img.offsetHeight;
    img.style.width = (w / 2) + "px";
    slider = document.createElement("DIV");
    slider.setAttribute("class", "img-comp-slider");
    img.parentElement.insertBefore(slider, img);
    slider.style.top = (h / 2) - (slider.offsetHeight / 2) + "px";
    slider.style.left = (w / 2) - (slider.offsetWidth / 2) + "px";
    slider.addEventListener("mousedown", slideReady);
    window.addEventListener("mouseup", slideFinish);
    slider.addEventListener("touchstart", slideReady);
    window.addEventListener("touchend", slideFinish);
    function slideReady(e) {
      e.preventDefault();
      clicked = 1;
      window.addEventListener("mousemove", slideMove);
      window.addEventListener("touchmove", slideMove);
    }
    function slideFinish() {
      clicked = 0;
    }
    function slideMove(e) {
      var pos;
      if (clicked == 0) return false;
      pos = getCursorPos(e)
      if (pos < 0) pos = 0;
      if (pos > w) pos = w;
      slide(pos);
    }
    function getCursorPos(e) {
      var a, x = 0;
      e = (e.changedTouches) ? e.changedTouches[0] : e;
      a = img.getBoundingClientRect();
      x = e.pageX - a.left;
      x = x - window.pageXOffset;
      return x;
    }
    function slide(x) {
      img.style.width = x + "px";
      slider.style.left = img.offsetWidth - (slider.offsetWidth / 2) + "px";
    }
  }
}
