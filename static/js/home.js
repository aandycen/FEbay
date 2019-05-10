var accountLink = document.getElementById('account');
var cartLink = document.getElementById('cart');
var registerLink = document.getElementById('signUp');
var loginLink = document.getElementById('logIn');
var postListingLink = document.getElementById('postListing');
var logOutLink = document.getElementById('logOut');

var listingsTable = document.getElementById('listingsTable');
var listingsTableBody = document.getElementById('listingsTableBody');

var addToCartBtn = document.getElementById('addToCartBtn');

var ascendingPriceOption = document.getElementById('ascendingPrice');
var descendingPriceOption = document.getElementById('descendingPrice');
var ascendingQuanitityOption = document.getElementById('ascendingQuantity');
var descendingQuantityOption = document.getElementById('descendingQuantity');
var ascendingRatingsOption = document.getElementById('ascendingRatings');
var descendingRatingsOption = document.getElementById('descendingRatings');

var snackbar = document.getElementById('snackbar');
var searchBar = document.getElementById('searchBar');

var items = [];
var itemTracker = {};

var PRICE = 'price';
var QUANTITY = 'quantity';
var RATING = 'rating';
var ASC = 'ASC';
var DESC = 'DESC';


errorAlert = function() {
	var x = document.getElementById("snackbar");
	x.className = "show";
	setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

loadLinks = function(){
    if (sessionStorage.getItem('user') != null){
	registerLink.className = 'nav-link not-displayed';
	loginLink.className = 'nav-link not-displayed';
    }else{
	accountLink.className = 'nav-link not-displayed';
	cartLink.className = 'nav-link not-displayed';
	postListingLink.className = 'nav-link not-displayed';
	logOutLink.className = 'nav-link not-displayed';
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
	imageWrapper.className = "text-center";
	let itemName = document.createElement('td');
	itemName.className = "text-center";
	let sellerEmail = document.createElement('td');
	sellerEmail.className = "text-center";
	let sellerRating = document.createElement('td');
	sellerRating.className = "text-center";
	let quantity = document.createElement('td');
	quantity.className = "text-center";
	let price = document.createElement('td');
	price.className = "text-center";
	let drpWrapper = document.createElement('td');

	let image = document.createElement('img');
	let quantityDrp = document.createElement('select');

	itemName.innerText = itemInfo['Name'];
	sellerEmail.innerText = itemInfo['Email'];

	let sellerInfo = makeApiCall('/account', 'POST', {'email': itemInfo['Email']});
	sellerRating.innerText = sellerInfo['Rating'];
	quantity.innerText = itemInfo['Quantity'];
	price.innerText = "$"+itemInfo['Price'];

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
	var itemAddedToCart = 0;
    let userEmail = JSON.parse(sessionStorage.getItem('user'))['Email'];
    for (let key in itemTracker){
	if (itemTracker[key] != '0'){
		itemAddedToCart = 1;
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
    if (itemAddedToCart == 0) {
    	snackbar.innerText = "No items were added to cart";
    	errorAlert();
    }
    else {
    	location.reload();
    }
}

logOutLink.onclick = function(event){
    event.preventDefault();
    console.log("Prevented Default Action");
    sessionStorage.clear();
    redirect('/');
}

searchListings = function(searchQuery){
		let params = {
		'keyword': searchQuery
		};
    let itemListings = makeApiCall('/get_item_keyword', 'POST', params);
		console.log(itemListings);
		listingsTableBody.innerHTML = "";
    for (let i = 0; i < itemListings.length; i++){
			let itemInfo = itemListings[i];
			let itemRow = document.createElement('tr');

			let imageWrapper = document.createElement('td');
			imageWrapper.className = "text-center";
			let itemName = document.createElement('td');
			itemName.className = "text-center";
			let sellerEmail = document.createElement('td');
			sellerEmail.className = "text-center";
			let sellerRating = document.createElement('td');
			sellerRating.className = "text-center";
			let quantity = document.createElement('td');
			quantity.className = "text-center";
			let price = document.createElement('td');
			price.className = "text-center";
			let drpWrapper = document.createElement('td');

			let image = document.createElement('img');
			let quantityDrp = document.createElement('select');

			itemName.innerText = itemInfo['Name'];
			sellerEmail.innerText = itemInfo['Email'];

			let sellerInfo = makeApiCall('/account', 'POST', {'email': itemInfo['Email']});
			sellerRating.innerText = sellerInfo['Rating'];
			quantity.innerText = itemInfo['Quantity'];
			price.innerText = "$"+itemInfo['Price'];

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
		}
}

setup = function(){
    loadLinks();
    loadItems();
    loadItemHTML();

    addToCartBtn.addEventListener('click', addToCart);
    var loadItemsInOrder = function(comparer, order){
	while (listingsTableBody.firstChild){
	    listingsTableBody.removeChild(listingsTableBody.firstChild);
	}
	items = makeApiCall('/sort_item_' + comparer, 'POST', {'order': order});
	loadItemHTML();
	console.log('hello');
    }

    ascendingPriceOption.addEventListener('click', loadItemsInOrder.bind(this, PRICE, ASC));
    descendingPriceOption.addEventListener('click', loadItemsInOrder.bind(this, PRICE, DESC));
    ascendingQuanitityOption.addEventListener('click', loadItemsInOrder.bind(this, QUANTITY, ASC));
    descendingQuantityOption.addEventListener('click', loadItemsInOrder.bind(this, QUANTITY, DESC));
    ascendingRatingsOption.addEventListener('click', loadItemsInOrder.bind(this, RATING, ASC));
    descendingRatingsOption.addEventListener('click', loadItemsInOrder.bind(this, RATING, DESC));
		searchBar.addEventListener('keyup', function(e){
		    if (e.keyCode == 13){
			e.preventDefault();

			let searchBarQuery = searchBar.value;
			searchBar.value = "";
			searchListings(searchBarQuery);

		    }
		});
}

setup();
