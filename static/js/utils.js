makeApiCall = function(url, method, obj){
    var xhr = new XMLHttpRequest();
    xhr.open(method || 'GET', url, false);
    xhr.send(JSON.stringify(obj));
    
    return xhr.responseText ? JSON.parse(xhr.responseText) : null;
}
