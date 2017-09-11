$(document).ready(function(){
  $("#search").click(function(){
    $("#searchtext").val = $("#searchtext").val().trim();
    if( ! content)  return false;
    var url = '/s';
    $("form").attr("action", url).submit();
  });
  $(document).on("keydown",function(e){
    if(e.keyCode==13){
      $("#search").trigger("click");
  }});

});
