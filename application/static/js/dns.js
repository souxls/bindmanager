$(document).ready(function(){
  $("form").submit(function(e){
    e.preventDefault()
    if( ! $(this).parsley().isValid()) return false;
    var postdata = {};
    var url = window.location.pathname;
    $(".even.pointer").find("input,select").each(function(){
      var name = $(this).attr("name");
      var value = $(this).val();
      postdata[name] = value;
    });
    $.ajax({
      type:"post",
      cache:false,
      data: postdata,
      dataType:'json',
      url: url,
      timeout:2000,
      success:function(data){
      var status = data.status
      if(status == "fail"){ console.log(data.error); return false};
      $(".even.pointer").find("input,select,button,p").addClass("hidden");
      $.each(postdata, function(name, value){
        $(".even.pointer").find("span[name="+name+"]").text(value);
        if(name === "domain"){
          var href = window.location.pathname + value;
          var content = '<a href="' + href + '">' + value + '</a>';
          $(".even.pointer").find("span").append(content);
          console.log("222")
        }
        $(".even.pointer").find("span,a").removeClass("hidden");
      });
      $(".even.pointer").attr("class", "odd pointer");
   }});

    $(document).on("keydown",function(e){
      if(e.keyCode==13){
        $("#save").trigger("click");
    }});
  });

  $("span").on('click', function(){
    if(window.location.pathname !== "/dns/"){ 
      $(this).parents("tr").attr("class","even pointer");
      $(this).parents("tr").find("input,select,button,p").removeClass("hidden");
      $(this).parents("tr").find("span,a").addClass("hidden");
  }});

  $("#addrecord").on("click", function(){
      var trhtml = $("tr.odd.pointer").first().clone();
      $(trhtml).attr("class","even pointer").prependTo("tbody");
      $(".even.pointer").find("span").addClass("hidden");
      $(".even.pointer").find("span").text("");
      $(".even.pointer").find("input").attr("placeholder", "");
      $(".even.pointer").find("input").attr("value", "");
      $(".even.pointer").find("input,select,button,p").removeClass("hidden");
    });

  $("div").on("click", "p[name=cancel]", function(){
    if($(".even.pointer").find("span[name=host]").text() == "" |
       $(".even.pointer").find("span[name=host]").text() == "undefied") {
      console.log("2222");
      console.log($(".even.pointer").find("span[name=host]").text());
      $(this).parents("tr").remove();
    }else{
      $(this).parents("tr").find("input,select,button,p").addClass("hidden");
      $(this).parents("tr").find("span,a").removeClass("hidden");
      $(this).parents("tr").attr("class", "odd pointer");
   }
    return false;
  });

  $("a[name=delete]").on('click', function(){
    modalConform($(this));
  });
  
  $("#deletes").on('click', function(){
    $("div").find('.checked').each(function(){
      modalConform($(this));
    });
  });
  
  $("#search").click(function(){
    var text = $("#searchtext").val().trim();
    if(window.location.search){
      window.location = window.location.pathname + '?wd=' + text;
    }else{
      window.location = window.location.pathname + '/s?wd=' + text;
  }});
});

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
        $("#message").text(data.message)
          .show()
          .fadeOut(3000);
      }else{
        $("#message").text(data.error)
          .show()
          .fadeOut(3000);
  }}}});
}

function modalConform(id){
  var cid = id
  var urlpath = window.location.pathname + '/delete'
  $("#conform").click('hide.bs.modal', function(){
    delTr(cid, urlpath);
    $("#conformmodel").modal('hide');
  });
}
