$(document).ready(function() {
//  $( "#start" ).datepicker({dateFormat: 'dd/mm/yy'});
  $( "#end" ).datepicker({dateFormat: 'dd/mm/yy'});
  var date = [];
  $("#submit").click(function(x) {
//    console.log($("#form #start").val())
//    date.push($("#form #start").val().split("/"));
    date.push($("#form #end").val().split("/"));
  });
});