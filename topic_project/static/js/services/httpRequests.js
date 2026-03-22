/**
 * Does an asynchronous HTTP GET request
 * @param  {string} url [url to call]
 * @param  {(a: Object) => any} callback [callback when we receive the response]
 * @return {void}
 */
export function httpGetAsync(url, callback) {
    let request = new XMLHttpRequest();
    request.onreadystatechange = function() { 
        if (request.readyState == 4 && request.status == 200) {
            console.log(request.responseText)
            callback(JSON.parse(request.responseText).data);
        }
            
    }
    
    request.open("GET", url, true); // true for asynchronous 
    request.send(null);
}
