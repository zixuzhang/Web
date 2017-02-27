/**
 * Created by zxjd on 17-2-8.
 */
$('#container').jstree({
    'core' : {
      'data' : {
        "url" : "/get_json/{{ company_name }}",
        "dataType" : "json"
      }
    }
});
$('#container').on("changed.jstree", function (e, data){
    var currentNode = data.instance.get_selected(true)[0].text;
// {#    alert(currentNode)#}
    var path = data.instance.get_path(data.node,"/");
// {#    alert(path);#}
    var data = { "tag": path }
    $.ajax({
        type : "get",
        url : '/query',
        data : data,
        datatype: 'json',
        success:function (msg) {
// {#            alert( "Data Saved: " + msg.count );#}
            $('form').attr('id', path)
            $('#files').empty()
            $('#file_count').text(currentNode + '：' + msg.count)
            $.each(msg.lists, function (i, item) {
// {#                alert(item.filename)#}
                $('#files').append("<li><a href=/" + item.file_id + ">" + item.filename + "</a></li>" +
                    "<a href=\"/" + item.file_id + "/delete\" class=\"label label-danger\">删除</a>" +
                        "<a href=\"/" + item.file_id +  "/update\" class=\"label label-warning\">重新上传</a>"
                );
            })
        }
    })
});