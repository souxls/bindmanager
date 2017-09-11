$(document).ready(function(){
  $("form").submit(function(e){
    e.preventDefault()
    if( ! $(this).parsley().isValid()) return false;
    var encrypt = new JSEncrypt();
    $("#username").val = $.trim("#username");
    $("#password").val = $.trim("#password");
    encrypt.setPublicKey($('#pubkey').val());
    var password = encrypt.encrypt($('#password').val());
    postdata = $("form").serializeArray();
    postdata[1].value = password;
  $.ajax({
    type:"post",
    cache:false,
    data: postdata,
    dataType:'json',
    url: window.location.pathname,
    timeout:2000,
    success:function(data){
      if(data.status == "success"){
        window.location = data.url;
        return;
      }else{
        $("#message").text(data.error)
          .show()
          .fadeOut(3000);
  }}}})});

  $(document).on("keydown",function(e){
    if(e.keyCode==13){
      $("#login").trigger("click");
  }});
});
