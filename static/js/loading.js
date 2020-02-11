function showDiv() {
  document.getElementById('ZbxReport').style.display = "none";
  document.getElementById('loadingGif').style.display = "block";
  document.getElementById('CloseModal').style.display = "none";
  var modal = document.getElementById('id01');
//  document.getElementById('checkHost').disabled = true;
//  document.getElementById('checkTemplate').disabled = true;
//  document.getElementById('checkHostgroup').disabled = true;
//  document.getElementById('checkAction').disabled = true;
  document.getElementById('zbxHostCheck').disabled = true;
  document.getElementById('zbxServerForm').disabled = true;


  window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "block";
    }
  }

}