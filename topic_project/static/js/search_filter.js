import {CATEGORIES} from "./constants/categories.js";

const filterBar = document.getElementById("search-filter");
// const searchBar = document.getElementById("search-box").getElementsByTagName("input")[0];

let tools = {};
// populating the div bar
for (const [key, value] of Object.entries(CATEGORIES)) {
    tools[key] = [];
    filterBar.innerHTML += `<button>${value}</button>`;
}

let buttons = filterBar.getElementsByTagName("button");

for (const button of buttons) {
    let toggledOn = false;
    const defaultColour = button.style.background;

    button.addEventListener("click", () => {
        toggledOn = !toggledOn;
        button.style.background = toggledOn? "#757575": defaultColour;
    });
}