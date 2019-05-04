var accountLink = document.getElementById('account');
var cartLink = document.getElementById('cart');
var registerLink = document.getElementById('signUp');
var loginLink = document.getElementById('logIn');

var items = [];
loadLinks = function(){
    
    if (sessionStorage.getItem('user') != null){
	registerLink.className = 'nav-link not-displayed';
	loginLink.className = 'nav-link not-displayed';
    }else{
	accountLink.className = 'nav-link not-displayed';
	cartLink.className = 'nav-link not-displayed';
    }
}

loadItems = function(){
    items = makeApiCall('/items', 'GET', null);
    //makeApiCall('/link_for_item', 'POST', {'id': <id>});
    
}

loadLinks();
