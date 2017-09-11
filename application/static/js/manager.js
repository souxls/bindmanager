$(document).ready(function(){
  $("a[name=delete]").on('click', function(){
    modalConform($(this));
  });
});

function modalConform(id){
  var cid = id
  var urlpath = window.location.pathname + '/delete'
  $("#conform").click('hide.bs.modal', function(){
    delTr(cid, urlpath);
    $("#conformmodel").modal('hide');
  });
}

function delTr(nowTr, url){
  var spans = {};
  $(nowTr).parents("tr").children().children("span").each(function(){
    var id = $(this).attr('name');
    var value = $(this).text();
    spans[id] = value;
  });
  postdata = JSON.stringify(spans);
  $.ajax({
    type: "POST",
    cache: false,
    url: url,
    data: postdata,
    dataType: "json",
    contentType: "application/json",
    timeout: 2000,
    success: function(data){
      if(data.status == "success"){
        $(nowTr).parents("tr").remove();
      }else{
        $("#message").text(data.error)
          .show()
          .fadeOut(3000);
  }}});
}
