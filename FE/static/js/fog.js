const fileInput = document.getElementById("fileInput");
const uploadedVideo = document.getElementById("uploadedVideo");
const uploadedImage = document.getElementById("uploadedImage");
const upload = document.querySelector('.uploaded-content')
const progressBar = document.querySelector('.progress-bar');

fileInput.addEventListener('change', function () {
  const selectedFile = fileInput.files[0];
  if (selectedFile) {
    if (selectedFile.type.startsWith("image/")) {
      // Selected file is an image
      uploadedVideo.style.display = "none";
      uploadedImage.style.display = "block";
      uploadedImage.src = URL.createObjectURL(selectedFile);
    } else if (selectedFile.type.startsWith("video/")) {
      // Selected file is a video
      uploadedImage.style.display = "none";
      uploadedVideo.style.display = "block";
      uploadedVideo.src = URL.createObjectURL(selectedFile);
    } else {
      alert("Please upload an image or a video file.");
    }
  }
});