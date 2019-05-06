var accountLink = document.getElementById('account');
var cartLink = document.getElementById('cart');
var registerLink = document.getElementById('signUp');
var loginLink = document.getElementById('logIn');
var postListingLink = document.getElementById('postListing');

var listingsTable = document.getElementById('listingsTable');
var listingsTableBody = document.getElementById('listingsTableBody');

var addToCartBtn = document.getElementById('addToCartBtn');

var items = [];
var itemTracker = {};
loadLinks = function(){
    
    if (sessionStorage.getItem('user') != null){
	registerLink.className = 'nav-link not-displayed';
	loginLink.className = 'nav-link not-displayed';
    }else{
	accountLink.className = 'nav-link not-displayed';
	cartLink.className = 'nav-link not-displayed';
	postListingLink.className = 'nav-link not-displayed';
	
    }
}

loadItems = function(){
    items = makeApiCall('/items', 'GET', null);
    itemTracker = {};
    for (let i = 0; i < items.length; i++){
	itemTracker[items[i]['ItemID']] = 0;
    }
}

loadItemHTML = function(){
    for(let i = 0; i < items.length; i++){
	let itemInfo = items[i];
	let itemRow = document.createElement('tr');

	let imageWrapper = document.createElement('td');
	let itemName = document.createElement('td');
	let sellerEmail = document.createElement('td');
	let sellerRating = document.createElement('td');
	let quantity = document.createElement('td');
	let price = document.createElement('td');
	let drpWrapper = document.createElement('td');
	
	let image = document.createElement('img');
	let quantityDrp = document.createElement('select');
	
	itemName.innerText = itemInfo['Name'];
	sellerEmail.innerText = itemInfo['Email'];

	let sellerInfo = makeApiCall('/account', 'POST', {'email': itemInfo['Email']});
	sellerRating.innerText = sellerInfo['Rating'];
	quantity.innerText = itemInfo['Quantity'];
	price.innerText = itemInfo['Price'];

	image.src = makeApiCall('/link_for_item', 'POST', {'id': itemInfo['ItemID']});
	image.style.width = '100px';
	//image.style.height = '100px';
	imageWrapper.append(image);
	
	quantityDrp.className = 'custom-select';
	let defaultOption = document.createElement('option');
	defaultOption.selected = true;
	defaultOption.innerText = 0;
	quantityDrp.appendChild(defaultOption);
	for (let j = 1; j <= itemInfo['Quantity']; j++){
	    let qtOption = document.createElement('option');
	    qtOption.innerText = j;
	    quantityDrp.appendChild(qtOption);
	}
	
	var updateItemTracker = function(itemId, quantityDrpObj){
	    itemTracker[itemId] = quantityDrpObj.value;
	    console.log(itemTracker);
	};
	
	quantityDrp.addEventListener('change', updateItemTracker.bind(this, itemInfo['ItemID'], quantityDrp));
	
	drpWrapper.appendChild(quantityDrp);
	
	itemRow.appendChild(imageWrapper);
	itemRow.appendChild(itemName);
	itemRow.appendChild(sellerEmail);
	itemRow.appendChild(sellerRating);
	itemRow.appendChild(quantity);
	itemRow.appendChild(price);
	itemRow.appendChild(drpWrapper);

	listingsTableBody.appendChild(itemRow);
	//listingsTable.appendChild(listingsTableBody);
    }
    //makeApiCall('/link_for_item', 'POST', {'id': <id>});   

}

addToCart = function(){
    let userEmail = JSON.parse(sessionStorage.getItem('user'))['Email'];
    for (let key in itemTracker){
	if (itemTracker[key] != '0'){
	    
	    let params = {
		'id': key,
		'quantity' : parseInt(itemTracker[key]),
		'email' : userEmail
	    };
	    console.log(params);
	    let res = makeApiCall('/add_to_cart', 'POST', params);
	    if (!res['Success']){
		console.log(res['error']);
	    }
	}
    }
    location.reload();
}

setup = function(){
    loadLinks();
    loadItems();
    loadItemHTML();
    
    addToCartBtn.addEventListener('click', addToCart);
    
}

setup();
