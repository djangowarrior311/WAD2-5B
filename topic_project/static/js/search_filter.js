import { httpGetAsync } from "/static/js/services/httpRequests.js";


const filterBar = document.getElementById("search-filter");
const resultsDiv = document.getElementById("results");
const searchBar = document.querySelector(".search-box input");

// search filters
const buttons = [];
const filtersApplied = {};

let cachedResults = {
    data: [],
    total: 0
};

function formatSearchURL(request, offset) {
    return `topic/home/get_search_results?request=${request}&offset=${offset}`;
}

function populateDivBar(categories) {
    filterBar.innerHTML = "";
    filterBar.appendChild(document.createElement("p")).textContent = "Filter by tag:";

    for (const value of categories.data) {
        const button = document.createElement("button");
        button.textContent = value;
        filterBar.appendChild(button);
        buttons.push(button);

        // default state
        let toggledOn = true;
        filtersApplied[value] = true;
        button.style.opacity = "1";

        // toggle behaviour
        button.addEventListener("click", () => {
            window.location.href = `/topic/tag/${value}`;
        });

    }
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

function addResult(tool) {
    for (const tag of tool.tags) {
        if (filtersApplied[tag] === false) return;
    }
    resultsDiv.innerHTML += `<li><a href="${tool.review_slug}">${tool.name}</a></li>`;
}

function renderPageButtons() {
    pageButtonDiv.textContent = "";
    for (const element of pageButtons) {
        pageButtonDiv.appendChild(element);
    }
}

function disableArrows() {
    rightArrowButton.disabled = currentPage > pages - 2;
    leftArrowButton.disabled = currentPage === 0;
}

function pageButtonClick(newPageNumber) {
    currentPage = newPageNumber;
    disableArrows();
    httpGetAsync(formatSearchURL(prevRequest, RESULTS_PER_PAGE * newPageNumber), updateResults);
}

function addPageButton(pageNumber) {
    const button = document.createElement("button");
    button.textContent = String(pageNumber + 1);
    button.disabled = pageNumber === currentPage;

    button.addEventListener("click", () => pageButtonClick(pageNumber));
    pageButtons.push(button);
}

function updatePageButtons(totalResults) {
    pages = Math.floor(totalResults / RESULTS_PER_PAGE);
    disableArrows();
    pageButtons.length = 0;

    for (let i = 0; i < pages; i++) {
        addPageButton(i);
    }
    renderPageButtons();
}

function updateResults(results) {
    cachedResults = results;
    const tools = results.data;
    const totalAvailable = results.total;

    updatePageButtons(totalAvailable);

    resultsDiv.innerHTML = "";
    for (let i = 0; i < Math.min(tools.length, RESULTS_PER_PAGE); i++) {
        addResult(tools[i]);
    }
}

function search(event) {
    if (event.key !== "Enter") return;

    prevRequest = searchBar.value.toUpperCase();
    httpGetAsync(formatSearchURL(prevRequest, RESULTS_PER_PAGE * currentPage), updateResults);
}

// initial load
httpGetAsync("/topic/home/get_tags", populateDivBar);
updatePageButtons(0);

rightArrowButton.addEventListener("click", () => pageButtonClick(currentPage + 1));
leftArrowButton.addEventListener("click", () => pageButtonClick(currentPage - 1));
searchBar.addEventListener("keyup", search);
