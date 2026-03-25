import { httpGetAsync } from "./services/httpRequests.js";
const filterBar = document.getElementById("search-filter");
const resultsDiv = document.getElementById("results")
const searchBar = document.querySelector(".search-box input");


// search filters
// const searchURL = "topic/home/get_search_results?request={0}&offset={}"
const defaultDivInner = filterBar.innerHTML;
const buttons = [];
const filtersApplied = {};


function formatSearchURL(request, offset) {
    return `topic/home/get_search_results?request=${request}&offset=${offset}`
}


function populateDivBar(categories) {
    // populating the div bar
    filterBar.innerHTML = defaultDivInner;
    for (const [_, value] of Object.entries(categories.data)) {
        const button = document.createElement("button");
        const textNode = document.createTextNode(value);
        button.appendChild(textNode);
        filterBar.appendChild(button);
        buttons.push(button);
    }
}


// let buttons = filterBar.getElementsByTagName("button");


for (const button of buttons) {
    let toggledOn = false;
    const defaultColour = button.style.background;

    button.addEventListener("click", () => {
        toggledOn = !toggledOn;
        filtersApplied[button.textContent] = toggledOn;
        button.style.background = toggledOn? "#757575": defaultColour;
    });
}

// pagination
let pages = 0;
let currentPage = 0;
let prevRequest = "";
const RESULTS_PER_PAGE = 10;
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
    httpGetAsync(formatSearchURL(prevRequest, RESULTS_PER_PAGE * newPageNumber), updateResults)
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
        console.log(element.review_slug);
        addResult(element.name, element.review_slug);
    }
}


function search(event) {
    if (event.key != "Enter") {return;}
    let filter = searchBar.value.toUpperCase();
    prevRequest = filter;
    httpGetAsync(formatSearchURL(prevRequest, RESULTS_PER_PAGE * currentPage), updateResults)
}

// initially populate the pages
httpGetAsync("topic/home/get_tags", populateDivBar);
updatePageButtons(0);
rightArrowButton.addEventListener("click", () => pageButtonClick(currentPage + 1))
leftArrowButton.addEventListener("click", () => pageButtonClick(currentPage - 1));
searchBar.addEventListener("keyup", search)