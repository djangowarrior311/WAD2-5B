import { httpGetAsync } from "./services/httpRequests.js";
const filterBar = document.getElementById("search-filter");
const resultsDiv = document.getElementById("results")
const searchBar = document.querySelector(".search-box input");


// search filters
const defaultDivInner = filterBar.innerHTML;
let buttons = filterBar.getElementsByTagName("button");


function populateDivBar(categories) {
    // populating the div bar
    filterBar.innerHTML = defaultDivInner;
    for (const [key, value] of Object.entries(categories.data)) {
        tools[key] = [];
        filterBar.innerHTML += `<button>${value}</button>`;
    }
}


for (const button of buttons) {
    let toggledOn = false;
    const defaultColour = button.style.background;

    button.addEventListener("click", () => {
        toggledOn = !toggledOn;
        button.style.background = toggledOn? "#757575": defaultColour;
    });
}

// pagination
let pages = 0;
let currentPage = 0;
let prevRequest = "";
const RESULTS_PER_PAGE = 1;
const pageButtonDiv = document.querySelector("#pagination div");
const leftArrowButton = document.querySelector("#left-arrow");
const rightArrowButton = document.querySelector("#right-arrow");
const pageButtons = [];


function addResult(result, url) {
    resultsDiv.innerHTML += `<li><a href=${url}>${result}</a></li>`
}


function renderPageButtons() {
    pageButtonDiv.textContent = '';
    for (const element of pageButtons) {
        pageButtonDiv.appendChild(element);
    }
}


function disableArrows() {
    rightArrowButton.disabled = currentPage > pages - 2;
    leftArrowButton.disabled = currentPage == 0;
}


function pageButtonClick(newPageNumber) {
    currentPage = newPageNumber;
    disableArrows();
    httpGetAsync(`topic/home/get_search_results?request=${prevRequest}&offset=${RESULTS_PER_PAGE * newPageNumber}`, updateResults)
}


function addPageButton(pageNumber) {
    const button = document.createElement("button");
    const buttonLabel = document.createTextNode(String(pageNumber + 1));
    button.disabled = pageNumber == currentPage;
    button.addEventListener("click", () => {
        pageButtonClick(pageNumber);
    })
    button.appendChild(buttonLabel);
    pageButtons.push(button);
}


function updatePageButtons(totalResults) {
    pages = Math.floor(totalResults / RESULTS_PER_PAGE);
    disableArrows();
    // clear the array
    pageButtons.length = 0;
    for (let i = 0; i < pages; i++) {
        addPageButton(i);
    }
    renderPageButtons();
}


function updateResults(results) {
    const tools = results.data;
    // total tools in database for this queery (to figure out how many pages)
    const totalAvailable = results.total;
    updatePageButtons(totalAvailable);
    // what was actually returned
    const actualReceived = tools.length;
    resultsDiv.innerHTML = ""
    for (let i = 0; i < Math.min(actualReceived, RESULTS_PER_PAGE); i++) {
        const element = tools[i];
        addResult(element.name, element.url); // i think this needs to be changed so that it goes to the specific tool's tool.html page
                                                // been trying for a while, but can't figure out how to do it.
                                                // it should direct to topic:show_tool tool.slug or topic/tools/<slug:learning_tool_slug>/
    }
}


function search(event) {
    if (event.key != "Enter") {return;}

    let filter = searchBar.value.toUpperCase();
    prevRequest = filter;
    httpGetAsync(`topic/home/get_search_results?request=${prevRequest}&offset=${RESULTS_PER_PAGE * currentPage}`, updateResults)
}

// initially populate the pages
httpGetAsync("topic/home/get_tags", populateDivBar);
updatePageButtons(0);
rightArrowButton.addEventListener("click", () => pageButtonClick(currentPage + 1))
leftArrowButton.addEventListener("click", () => pageButtonClick(currentPage - 1));
searchBar.addEventListener("keyup", search)