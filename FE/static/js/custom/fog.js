const fileInput = document.querySelector('#fileInput')
const uploadedVideo = document.querySelector('#uploadedVideo')
const uploadedImage = document.querySelector('#uploadedImage')
const uploadText = document.getElementById('uploadText')
const uploadedContent = document.querySelector('.uploaded-content')
const loading = document.querySelector('#loading-zone')
const uploadBtn = document.querySelector('#uploadBtn label')

loading.style.display = 'none'

// ======= 예외처리 =======

// [E1. 파일의 크기가 너무 큰 경우]
const fileSizeException = function (selectedFile){
    const allowedFileSize = 2000000000 //2GB(2000000000) 이상
    if(selectedFile.size >= allowedFileSize){ 
        console.log('파일의 크기가 너무 큽니다')
        uploadText.innerHTML = '파일의 크기가 너무 큽니다'
        uploadText.style.color = 'red';
        return 0;
    }
}

// [E2. 파일의 확장자가 맞지 않는 경우]
const fileExtensionException = function (selectedFile) {
    // 필요한 확장자만 사용하시면 됩니다.
    const allowedExtensions = ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi']; 
    const fileExtension = selectedFile.name.split('.').pop().toLowerCase(); 

    if (!allowedExtensions.includes(fileExtension)) {
        uploadText.innerHTML = '파일의 확장자가 맞지 않습니다. 확장자를 확인해주세요.';
        fileInput.value = '';
        return 0
    }
};

// [E3. 업로드 중에 중지된 경우]
const uploadInterruptedException = function () {
    if (!fileInput.files.length) {
        uploadText.innerHTML = '파일 업로드가 중지되었습니다. 다시 시도해 주세요.';
        return 0;
    }
};

// [E4. 중지된 업로드를 재개할 경우]
// 1. 파일을 다시 업로드할 수 있는 재업로드 버튼(혹은 문구)를 제공한다.
const provideRetryOption = function () {
    uploadBtn.innerHTML = 'REUPLOAD'
    uploadBtn.addEventListener('click',()=>{
        location.reload(true);
    })
};

// [E5. 파일 업로딩 시, 제한 시간을 초과할 경우]
// 1. 파일 업로드 시 시간제한을 설정하고 해당 시간을 넘어서까지 업로드가 되지 않는다면 위의 에러 메시지를 출력. 재업로드 버튼을 제공한다.
const uploadTimeoutException = function () {
    const timeoutLimit = 6000;
    
    if (Date.now() - uploadStartTime > timeoutLimit) {
        uploadText.innerHTML = '파일 업로딩 시간이 초과되었습니다. 재업로드 버튼을 눌러 다시 시도해 주세요.';
        provideRetryOption();
        
        return 0;
    } 
};

let uploadStartTime;

// ======= 파일 업로드 =======
uploadBtn.addEventListener('click', function () {
    uploadedContent.style.display = 'none';

    fileInput.addEventListener('change', function () {
        const selectedFile = fileInput.files[0];

        if (fileSizeException(selectedFile) === 0) {
            console.log('break');
            return 0;
        }

        if (fileExtensionException(selectedFile) === 0) {
            console.log('break');
            return 0;
        }

        if (uploadInterruptedException() === 0) {
            console.log('break');
            return 0;
        }

        uploadStartTime = Date.now(); // Record the upload start time

        loading.style.display = 'block';
        setTimeout(function () {
            uploadText.style.display = 'none'
                if (selectedFile.type.startsWith('image/')) {
                    uploadedContent.style.display = 'block'
                    uploadedImage.style.display = 'block'
                    uploadedImage.src = URL.createObjectURL(selectedFile)
                } else if (selectedFile.type.startsWith('video/')) {
                    uploadedContent.style.display = 'block'
                    uploadedVideo.style.display = 'block'
                    uploadedVideo.src = URL.createObjectURL(selectedFile)
                } else {
                    alert('Please upload an image or a video file.')
                }

            // [E5. 파일 업로딩 시, 제한 시간을 초과할 경우]
            if (uploadTimeoutException() === 0) {
                console.log('break');
                loading.style.display = 'none';
                return 0;
            }
            loading.style.display = 'none';
        }, 5000);
    });
});

