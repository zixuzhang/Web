/**
 * Created by zxjd on 17-2-9.
 */
// {#高亮#}
// {#    var keyword = '{{ search_name }}'#}
// {#    $('.col-md-8').mark(keyword)#}
$(document).ready(function () {
    $('li').click(function () {
        var file_id =$(this).attr('id')
        var data = {'file_id': file_id}
        $.ajax({
            type:'GET',
            url:'/query_html',
// {#            cache:false,#}
            data:data,
            datatype:'json',
            beforeSend:function (XMLHttpRequest) {
                $('#filename').html('加载中：<img src="/static/loading1.gif"/>')
// {#                $('iframe').removeAttr("srcdoc")#}
// {#                $('iframe').attr('src',"/static/loading.html")#}
            },
            success:function (msg) {
                $('#filename').text('预览:'+msg.filename);
// {#                $('iframe').removeAttr("src")#}
                $('iframe').attr('srcdoc', msg.html1)
            }
        })
    })
 });