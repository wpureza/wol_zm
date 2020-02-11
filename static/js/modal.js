// Get the modal
var modal = document.getElementById('id01');
modal.style.display = "block";

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

function zbxServerFunction() {
  // Get the checkbox
  var checkBox = document.getElementById("zbxServerCheck");
  // Get the output text
  var zbxServerForm = document.getElementById("zbxServerForm");

  // If the checkbox is checked, display the output text
  if (checkBox.checked == true){
    zbxServerForm.style.display = "block";
  } else {
    zbxServerForm.style.display = "none";
  }
}

function zbxHostFunction() {
  // Get the checkbox
  var checkBox = document.getElementById("zbxHostCheck");
  // Get the output text
  var zbxServerForm = document.getElementById("zbxServerForm");

  // If the checkbox is checked, display the output text
  if (checkBox.checked == true){
    zbxServerForm.style.display = "none";
  }
}