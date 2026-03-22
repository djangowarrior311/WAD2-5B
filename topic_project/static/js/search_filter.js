import { httpGetAsync } from "./services/httpRequests.js";
const filterBar = document.getElementById("search-filter");
const resultsDiv = document.getElementById("results")
const searchBar = document.querySelector("#search-filter p");

let tools = {};


const defaultDivInner = filterBar.innerHTML;


function populateDivBar(categories) {
    // populating the div bar
    filterBar.innerHTML = defaultDivInner;
    for (const [key, value] of Object.entries(categories)) {
        tools[key] = [];
        filterBar.innerHTML += `<button>${value}</button>`;
    }
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


function addResult(result, url) {
    resultsDiv.innerHTML += `
        <li><a href=${url}>${result}</a></li>
    `
}


function updateResults(results) {
    resultsDiv.innerHTML = ""
    for (const result of results) {
        addResult(result)
    }
}


httpGetAsync("topic/home/get_tags", updateResults)


// triggered by html
function search() {
    let filter = searchBar.value.toUpperCase();
    let ul = document.getElementById("ul");
    let li = ul.getElementsByTagName("li");


}