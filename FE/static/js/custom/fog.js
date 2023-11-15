const fileInput = document.querySelector('#fileInput')
const uploadedVideo = document.querySelector('#uploadedVideo')
const uploadedImage = document.querySelector('#uploadedImage')
const uploadText = document.getElementById('uploadText')
const uploadedContent = document.querySelector('.uploaded-content')
const loading = document.querySelector('#loading-zone')
const uploadBtn = document.querySelector('#uploadBtn')

loading.style.display = 'none'


// 예외처리
// [E1. 파일의 크기가 너무 큰 경우]
// 1. 파일의 크기가 너무 큰 경우에는 ‘파일의 크기가 너무 큽니다’ 에러 메시지 표시
const fileSizeException = function (selectedFile){
    console.log(selectedFile)
    if(selectedFile.size == 400341){ //1GB(1000000000) 이상
        console.log('너무 높아')
        uploadText.innerHTML = '너무 높아!'
        
    }
}

// [E2. 파일의 확장자가 맞지 않는 경우]
// 2. ‘파일의 확장자가 맞지 않습니다. 확장자를 확인해주세요.’ 라는 에러 메시지 표시


// [E1. 업로드 중에 중지된 경우]
// 1. 중지 시, ‘파일 업로드가 중지되었습니다. 다시 시도해 주세요’ 에러 메시지 표시


// [E1. 중지된 업로드를 재개할 경우]
// 1. 파일을 다시 업로드할 수 있는 재업로드 버튼(혹은 문구)를 제공한다.


// [E1. 파일 업로딩 시, 제한 시간을 초과할 경우 ]
// 1. 파일 업로드 시 시간제한을 설정하고 해당 시간을 넘어서까지 업로드가 되지 않는다면 위의 에러 메시지를 출력. 재업로드 버튼을 제공한다.


// 파일 업로드
uploadBtn.addEventListener('click', function () {
    uploadedContent.style.display = 'none'
    fileInput.addEventListener('change', function () {
        const selectedFile = fileInput.files[0]
        if (selectedFile) {
            loading.style.display = 'block'
            setTimeout(function () {
                if (selectedFile.type.startsWith('image/')) {
                    uploadedContent.style.display = 'block'
                    uploadedImage.style.display = 'block'
                    uploadText.style.display = 'none'
                    uploadedImage.src = URL.createObjectURL(selectedFile)
                } else if (selectedFile.type.startsWith('video/')) {
                    uploadedContent.style.display = 'block'
                    uploadedVideo.style.display = 'block'
                    uploadText.style.display = 'none'
                    uploadedVideo.src = URL.createObjectURL(selectedFile)
                } else {
                    alert('Please upload an image or a video file.')
                }
                loading.style.display = 'none'
            }, 5000)
        }
        fileSizeException(selectedFile)
        console.log(selectedFile.size)
    })
})
