/**
 * Does an asynchronous HTTP GET request
 * @param  {string} url [url to call]
 * @param  {(a: Object) => any} callback [callback when we receive the response]
 * @return {void}
 */
export function httpGetAsync(url, callback) {
    let request = new XMLHttpRequest();
    request.onreadystatechange = function() { 
        if (request.readyState != 4) {return;}
        if (request.status != 200) {return;}
        callback(JSON.parse(request.responseText));        
    }
    
    request.open("GET", url); // true for asynchronous 
    request.send();
}
