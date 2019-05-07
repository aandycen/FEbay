var shoppingCartTableBody = document.getElementById('shoppingCartTableBody');
var totalPriceInCart = document.getElementById('totalPriceInCart');

var updateCartBtn = document.getElementById('updateCartBtn');
var proceedToCheckoutBtn = document.getElementById('proceedToCheckoutBtn');

var itemTracker = {};
var cart = {};

loadCart = function(){
    let user = JSON.parse(sessionStorage.getItem('user'));
    cart = makeApiCall('/get_shopping_cart', 'POST', {'email' : user['Email']});
    for (let i = 0; i < cart['items'].length; i++){

	itemTracker[cart['items'][i]['itemid']] = cart['items'][i]['quantity'];
    }
}

loadCartHTML = function(){
    let user = sessionStorage.getItem('user');
    let itemList = cart['items'];
    for (let i = 0; i < itemList.length; i++){
	let itemInfo = itemList[i];

	let itemRow = document.createElement('tr');

	let drpWrapper = document.createElement('td');
	let imageWrapper = document.createElement('td');
	let itemName = document.createElement('td');
	let sellerEmail = document.createElement('td');
	let price = document.createElement('td');

	let image = document.createElement('img');
	let quantityDrp = document.createElement('select');

  imageWrapper.className = "text-center"
  itemName.className = "text-center";
  itemName.innerText = itemInfo['name'];
  sellerEmail.className = "text-center";
	sellerEmail.innerText = itemInfo['seller'];
  price.className = "text-center";
  price.innerText = itemInfo['price'];

	image.src = makeApiCall('/link_for_item', 'POST', {'id': itemInfo['itemid']});
	image.style.width = '100px';
//	image.style.height = '100px';
	imageWrapper.append(image);

	quantityDrp.className = 'custom-select';
	for (let j = 0; j <= itemInfo['in_stock']; j++){

	    let qtOption = document.createElement('option');
	    qtOption.innerText = j;
	    if (j == itemInfo['quantity']){
		qtOption.selected = true;
	    }

	    quantityDrp.appendChild(qtOption);
	}

	var updateItemTracker = function(itemId, quantityDrpObj){
	    itemTracker[itemId] = parseInt(quantityDrpObj.value);
	    console.log(itemTracker);
	};

	quantityDrp.addEventListener('change', updateItemTracker.bind(this, itemInfo['itemid'], quantityDrp));

	drpWrapper.appendChild(quantityDrp);

	itemRow.appendChild(drpWrapper);
	itemRow.appendChild(imageWrapper);
	itemRow.appendChild(itemName);
	itemRow.appendChild(price);
	itemRow.appendChild(sellerEmail);


	shoppingCartTableBody.appendChild(itemRow);

    }
    totalPriceInCart.innerText = "Total Price: $" + cart['total'].toFixed(2);

}

updateCart = function(){
    let user = JSON.parse(sessionStorage.getItem('user'));
    for (id in itemTracker){
	params = {
	    'id': id,
	    'quantity': itemTracker[id],
	    'email': user['Email']

	};
	console.log(params);
	let res = makeApiCall('/update_cart', 'POST', params);
    }
    console.log("Updating Cart...");
    location.reload();
}

loadCart();
loadCartHTML();
proceedToCheckoutBtn.style.display = cart['items'].length == 0? 'none':'block'; 
updateCartBtn.addEventListener('click', updateCart);

