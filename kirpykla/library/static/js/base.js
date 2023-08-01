var isOptionsVisible = false;
var profile = document.getElementById("profile");
var options = document.getElementById("options");
var optionsTimeout;

profile.addEventListener("mouseenter", function() {
  isOptionsVisible = true;
  updateOptionsPosition();
  options.style.display = "block";
});

profile.addEventListener("mouseleave", function() {
  // Add a small delay before hiding the options pop-up
  optionsTimeout = setTimeout(function() {
    isOptionsVisible = false;
    options.style.display = "none";
  }, 200);
});

profile.addEventListener("mousemove", function(event) {
  if (isOptionsVisible) {
    updateOptionsPosition();
  }
});

options.addEventListener("mouseenter", function() {
  // Clear the timeout to prevent hiding the pop-up when mouse is over options
  clearTimeout(optionsTimeout);
});

function updateOptionsPosition() {
  var profilePicRect = profile.getBoundingClientRect();
  options.style.top = profilePicRect.bottom + "px";
  options.style.left = profilePicRect.left + "px";
  options.style.zIndex = "2";
}