"use-strict"
let announcement = document.getElementById("announcements")
// we only need to worry about one button 
let closeButton = announcement.getElementsByTagName("button")[0]

// TODO: remember user's preference, but show the announcement again if there's a new one. 

let defaultDisplay = announcement.style.display

closeButton.addEventListener("click", () => {
    announcement.style.display = "none";
})
