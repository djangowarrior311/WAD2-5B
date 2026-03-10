"use-strict"
let announcement = document.getElementById("announcements")
// we only need to worry about one button 
let closeButton = announcement.getElementsByTagName("button")[0]
let defaultDisplay = announcement.style.display

closeButton.addEventListener("click", () => {
    if (announcement.style.display === "none") {
        announcement.style.display = defaultDisplay;
    } else {
        announcement.style.display = "none";
  }
})
