
document.getElementById("profile").addEventListener("mousemove", function() {
  var options = document.getElementById("options");
  options.style.display = (options.style.display === "block") ? "none" : "block";

  var profilePic = document.getElementById("profile");
  var profilePicRect = profilePic.getBoundingClientRect();

  options.style.top = profilePicRect.bottom + "px";
  options.style.left = profilePicRect.left + "px";
});