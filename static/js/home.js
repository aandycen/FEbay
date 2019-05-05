var accountLink = document.getElementById('account');
var cartLink = document.getElementById('cart');
var registerLink = document.getElementById('signUp');
var loginLink = document.getElementById('logIn');

var listingsTable = document.getElementById('listingsTable');
var listingsTableBody = document.getElementById('listingsTableBody');
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
    for(let i = 0; i < items.length; i++){
	let itemInfo = items[i];
	let itemRow = document.createElement('tr');
	
	let itemName = document.createElement('td');
	let sellerEmail = document.createElement('td');
	let quantity = document.createElement('td');
	let price = document.createElement('td');
	let image = document.createElement('img');

	
	itemName.innerText = itemInfo['Name'];
	sellerEmail.innerText = itemInfo['Email'];
	quantity.innerText = itemInfo['Quantity'];
	price.innerText = itemInfo['Price'];

	image.src = makeApiCall('/link_for_item', 'POST', {'id': itemInfo['ItemID']});
	image.style.width = '100px';
	image.style.height = '100px';
	
	itemRow.appendChild(image);
	itemRow.appendChild(itemName);
	itemRow.appendChild(sellerEmail);
	itemRow.appendChild(quantity);
	itemRow.appendChild(price);


	listingsTableBody.appendChild(itemRow);
	listingsTable.appendChild(listingsTableBody);
    }
    //makeApiCall('/link_for_item', 'POST', {'id': <id>});
    
}

loadLinks();
loadItems();
