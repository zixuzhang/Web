/**
 * Created by zxjd on 17-2-8.
 */
// {#    计算MD5#}

document.getElementById('file').addEventListener('change', function () {
    var blobSlice = File.prototype.slice || File.prototype.mozSlice || File.prototype.webkitSlice,
        file = this.files[0],
        chunkSize = 2097152,                             // Read in chunks of 2MB
        chunks = Math.ceil(file.size / chunkSize),
        currentChunk = 0,
        spark = new SparkMD5.ArrayBuffer(),
        fileReader = new FileReader();
    fileReader.onload = function (e) {
        console.log('read chunk nr', currentChunk + 1, 'of', chunks);
        spark.append(e.target.result);                   // Append array buffer
        currentChunk++;
        if (currentChunk < chunks) {
            loadNext();
        } else {
            $('form').prop('id', spark.end());
        }
    };
    fileReader.onerror = function () {
        console.warn('oops, something went wrong.');
    };
    function loadNext() {
        var start = currentChunk * chunkSize,
            end = ((start + chunkSize) >= file.size) ? file.size : start + chunkSize;
        fileReader.readAsArrayBuffer(blobSlice.call(file, start, end));
    }
    loadNext();
});

$('#upload_library > form').on('submit', function (event) {
    // 显示进度条
    var flag = 0
    $('.progress').css('display', 'block');
    // 阻止元素发生默认的行为，此处用来阻止对表单的提交
    event.preventDefault();
    var formData = new FormData(this);
    var file_md5 = $('form').attr('id');
    formData.append('file_md5', file_md5);
    // jQuery Ajax 上传文件，关键在于设置：processData 和 contentType
    $.ajax({
        xhr: function () {
            var xhr = new XMLHttpRequest();
            xhr.upload.addEventListener('progress', function (e) {
                if (e.lengthComputable) {
                    var percent = Math.round(e.loaded * 100 / e.total);
                    $('.progress-bar').attr('aria-valuenow', percent).css('width', percent + '%').text(percent + '%');
                }
            });
            return xhr;
        },
        type: 'POST',
        url: '/upload',
        cache: false,
        // async: false,
        data: formData,
        // 告诉 jQuery 不要去处理发送的数据
        processData: false,
        // 告诉 jQuery 不要去设置 Content-Type 请求头
        // 因为这里是由 <form> 表单构造的 FormData 对象，且已经声明了属性 enctype="multipart/form-data"，所以设置为 false
        contentType: false
    }).done(function (res) {
        flag = 1
        alert(res);
        // window.location.reload()
    }).fail(function (res) {
        flag = 1
        alert('上传失败!');
        // window.location.reload()
    });
    if (flag == 0){
    window.onbeforeunload = function(){
        return "您的文章尚未保存！";
    }
}
});


