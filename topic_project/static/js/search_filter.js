import { httpGetAsync } from "./services/httpRequests.js";
const filterBar = document.getElementById("search-filter");
const resultsDiv = document.getElementById("results")
const searchBar = document.querySelector(".search-box input");

let currentPage = 0;
let prevRequest = "";
const RESULTS_PER_PAGE = 20;

const defaultDivInner = filterBar.innerHTML;


// pagination
const pageButtonDiv = document.querySelector("#pagination div");
const pageButtons = [];

function populateDivBar(categories) {
    // populating the div bar
    filterBar.innerHTML = defaultDivInner;
    for (const [key, value] of Object.entries(categories.data)) {
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
    console.log(`<li><a href=${url}>${result}</a></li>`);
    resultsDiv.innerHTML += `<li><a href=${url}>${result}</a></li>`
}


function renderPageButtons() {
    pageButtonDiv.textContent = '';
    for (const element of pageButtons) {
        pageButtonDiv.appendChild(element);
    }
}


function addPageButton(pageNumber) {
    const button = document.createElement("button");
    const buttonLabel = document.createTextNode(String(pageNumber + 1));
    button.addEventListener("click", () => {
        currentPage = pageNumber;
        httpGetAsync(`topic/home/get_search_results?request=${prevRequest}&offset=${RESULTS_PER_PAGE * pageNumber}`, updateResults)
    })
    button.appendChild(buttonLabel);
    pageButtons.push(button);
}


function updatePageButtons(totalResults) {
    const pagesNeeded = Math.floor(totalResults / RESULTS_PER_PAGE);
    pageButtons.length = 0;
    for (let i = 0; i < pagesNeeded; i++) {
        addPageButton(i);
    }
    renderPageButtons();
}


function updateResults(results) {
    console.log(results.data)
    const tools = results.data;
    // total tools in database for this queery (to figure out how many pages)
    const totalAvailable = results.total;
    updatePageButtons(totalAvailable);

    // what was actually returned
    const actualReceived = tools.length;
    resultsDiv.innerHTML = ""
    for (let i = 0; i < Math.min(actualReceived, RESULTS_PER_PAGE); i++) {
        const element = tools[i];
        addResult(element.name, element.url);
    }
}


httpGetAsync("topic/home/get_tags", populateDivBar);


// triggered by html
function search(event) {
    if (event.key != "Enter") {return;}

    let filter = searchBar.value.toUpperCase();
    // httpGetAsync("topic/home/")
    prevRequest = filter;
    httpGetAsync(`topic/home/get_search_results?request=${prevRequest}&offset=${RESULTS_PER_PAGE * currentPage}`, updateResults)
}


updatePageButtons(0);
searchBar.addEventListener("keyup", search)