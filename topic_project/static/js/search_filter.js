import {CATEGORIES} from "./constants/categories.js";

const filterBar = document.getElementById("search-filter");

// populating the div bar
for (const [key, value] of Object.entries(CATEGORIES)) {
//   console.log(`${key}: ${value}`);
    filterBar.innerHTML += `<button>${value}</button>`
}

let buttons = filterBar.getElementsByTagName("button")

for (const button of buttons) {
    let toggledOn = false;
    const defaultColour = button.style.background;
    button.addEventListener("click", () => {
        toggledOn = !toggledOn;
        button.style.background = toggledOn? "#757575": defaultColour;
    });
}