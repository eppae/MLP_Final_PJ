let checkboxes = document.getElementsByName("selected_boxes");
document.getElementById("check-all").addEventListener("change", function () {
  for (let i = 0; i < checkboxes.length; i++) {
    checkboxes[i].checked = this.checked;
  }
});

// 체크박스 삭제 기능
document.querySelector("form").addEventListener("submit", function (e) {
  var checkboxes = document.getElementsByName("selected_boxes");
  for (var i = 0; i < checkboxes.length; i++) {
    if (checkboxes[i].checked) {
      var row = checkboxes[i].closest("tr");
      row.parentNode.removeChild(row);
    }
  }
});

const blog_page_elements = document.getElementsByClassName("page-link");
Array.from(blog_page_elements).forEach(function (element) {
  element.addEventListener("click", function () {
    document.getElementById("page").value = this.dataset.page;
    document.getElementById("BoardSearch").submit();
  });
});
const btnSearch = document.getElementById("btnSearch");
btnSearch.addEventListener("click", function () {
  document.getElementById("contact_kw").value =
    document.getElementById("contact_search_kw").value;
  document.getElementById("page").value = 1;
  document.getElementById("BoardSearch").submit();
});
