/*
$(document).ready(function () {
  $('.toast').toast('show');
});

/* When the user clicks on the image, 
toggle between hiding and showing the dropdown content */
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function (event) {
  if (!event.target.matches('.navbar-img')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

// This is all for the toast
window.onload = function () {
  Toast("These are just simulators of the books. You are not able to read or purchase them. If so, visit Goodreads website for more info.", { origin: "top", delay: 8000 });
}

function Toast(text, options) {
  options = options || {};

  let delayToShow = 0, delayToRemove = 300;
  let timeout = options.delay || 3000;

  this.hideToast = function (node) {
    node.className += " hidden";
    setTimeout(function () { this.removeToast(node) }, delayToRemove);
  }
  this.showToast = function (node) {
    node.classList.toggle("hidden");
  }
  this.removeToast = function (node) {
    node.remove();
  }

  let div = document.createElement("div");
  div.className = "toast hidden " + options.origin;
  div.innerHTML = text;
  document.querySelector("body").appendChild(div);

  setTimeout(function () { this.showToast(div) }, delayToShow);
  setTimeout(function () { this.hideToast(div) }, timeout);
}