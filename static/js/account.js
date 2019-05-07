var updatePasswordBtn = document.getElementById('updatePasswordBtn');
var updateAddressBtn = document.getElementById('updateAddressBtn');
var shippingAddress = document.getElementById('shippingAddress');
var billingAddress = document.getElementById('billingAddress');
var password = document.getElementById('password');

var addCreditCardBtn = document.getElementById('addCreditCardBtn');
var CCN = document.getElementById('CCN');
var securityCode = document.getElementById('securityCode');
var expiryDate = document.getElementById('expiryDate');

var creditCardTable = document.getElementById('creditCardTable');
var creditCardTableBody = document.getElementById('creditCardTableBody');
var creditCardStatus = document.getElementById('creditCardStatus');

var ordersTable = document.getElementById('ordersTable');
var ordersTableBody = document.getElementById('ordersTableBody');
var snackbar = document.getElementById('snackbar');

var listingTableBody = document.getElementById('listingTableBody');

var reviewsAsSellerTableBody = document.getElementById('reviewsAsSellerTableBody');
var reviewsForOthersTableBody = document.getElementById('reviewsForOthersTableBody');


errorAlert = function() {
    var x = document.getElementById("snackbar");
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

update = function() {
    let user = JSON.parse(sessionStorage.getItem('user'));

    shipping = {
    	'info' : 'shipping',
    	'address' : shippingAddress.value,
    	'email' : user['Email']
    }
    billing = {
    	'info' : 'billing',
    	'address' : billingAddress.value,
    	'email' : user['Email']
    }
    pw = {
    	'info' : 'password',
    	'password' : password.value,
    	'email' : user['Email']
    }

    makeApiCall('/update_info', 'POST', shipping);
    makeApiCall('/update_info', 'POST', billing);
    let x = makeApiCall('/update_info', 'POST', pw);
    if (x['success'] == false) {
	snackbar.innerText = x['message'];
	errorAlert();
    }
    let res = makeApiCall('/account', 'POST', {'email': user['Email']})
    sessionStorage.setItem('user', JSON.stringify(res));
}

loadCreditCards = function(){
    let user = JSON.parse(sessionStorage.getItem('user'));

    creditCardTable.appendChild(document.createElement('tbody'));

    params = {'email' : user['Email']};
    let creditCardList = makeApiCall('/cards_from_user', 'POST', params);
    console.log(creditCardList);
    for (let i = 0; i < creditCardList.length; i++) {
        let cc = creditCardList[i];
        console.log(cc);
        addCreditCardHTML(cc['CCN'], cc['ExpiryDate']);
    }

}

loadInfo = function(){
    let user = JSON.parse(sessionStorage.getItem('user'));
    console.log(user['Shipping']);
    if (user['Shipping'] != null){
	shippingAddress.value = user['Shipping'];
    }
    if (user['Billing'] != null){
	billingAddress.value = user['Billing'];
    }
    //password.value = user['Password'];

    loadCreditCards();
}

deleteCreditCard = function(CCNumber, expiry, cvv){
    let user = JSON.parse(sessionStorage.getItem('user'));
    creditCard = {
    	'info' : 'creditcard',
    	'action' : 'remove',
    	'email' : user['Email'],
    	'ccn' : CCNumber,
    	'securitycode' : cvv,
    	'expirydate' : expiry
    };
    makeApiCall('/update_info', 'POST', creditCard);
}

addCreditCardHTML = function(CCNumber, expiry, cvv){
    let newCC = document.createElement('tr');

    let ccn = document.createElement('td');
    let exp = document.createElement('td');

    ccn.innerText = CCNumber;
    exp.innerText = expiry;

    let deleteBtnWrapper = document.createElement('td');
    let deleteBtn = document.createElement('button');
    let deleteBtnX = document.createElement('span')
    deleteBtn.className = "close";
    //deleteBtn.style.background = "rgb(202, 60, 60)";
    //deleteBtn.style.color = "rgb(255,255,255)";
    deleteBtnX.innerHTML = "&times;";
    var deleteCreditCardHTML = function(ccRow, ccn0, expiry0, cvv0) {
    	deleteCreditCard(ccn0, expiry0, cvv0);
    	console.log(creditCardTableBody);
    	creditCardTableBody.removeChild(ccRow);
    	console.log(ccRow);
    	console.log(creditCardTableBody);
    }

    newCC.appendChild(ccn);
    newCC.appendChild(exp);


    creditCardTableBody.appendChild(newCC);
    deleteBtnWrapper.appendChild(deleteBtn);
    deleteBtn.appendChild(deleteBtnX);
    newCC.appendChild(deleteBtnWrapper);
    deleteBtn.addEventListener('click', deleteCreditCardHTML.bind(this, newCC, CCNumber, expiry, cvv));
}

addCreditCard = function(){
    let user = JSON.parse(sessionStorage.getItem('user'));
    creditCard = {
    	'info' : 'creditcard',
    	'action' : 'add',
    	'email' : user['Email'],
    	'ccn' : CCN.value,
    	'securitycode' : securityCode.value,
    	'expirydate' : expiryDate.value
    };
    let res = makeApiCall('/update_info', 'POST', creditCard);
    if (res['success']){
	addCreditCardHTML(CCN.value, expiryDate.value, securityCode.value);
    }
    else {
	snackbar.innerText = res['message'];
	errorAlert();
    }
}

loadOrders = function(){
    let user = JSON.parse(sessionStorage.getItem('user'));
    let orderList = makeApiCall('/purchases_for_user', 'POST', {'email': user['Email']});

    for(let i = 0; i < orderList.length; i++){
	let order = orderList[i];
	let orderRow = document.createElement('tr');

	let orderDate = document.createElement('td');
	let itemDetails = document.createElement('td');
	let shippingAddress = document.createElement('td');
	let payment = document.createElement('td');
	let grandTotal = document.createElement('td');
	let tracking = document.createElement('td');
	let status = document.createElement('td');


	orderDate.className = "text-center";
	orderDate.innerText = order['OrderDate'].split(" ")[0];
	itemText = "";
	for (let i = 0; i < order['Items'].length; i++) {
	    itemText += order['Items'][i]['item'] + " : " + order['Items'][i]['quantity'] + " : " + order['Items'][i]['seller'] + "\n";
	}
	itemDetails.className = "text-center";
	itemDetails.innerText = itemText;
	shippingAddress.className = "text-center";
	shippingAddress.innerText = order['Shipping'];
	payment.innerText =  "************" + order['CCN'].toString().substr(12);
	grandTotal.className = "text-center";
	grandTotal.innerText = "$" + order['Price'];
	let shipment = makeApiCall('/get_shipment_by_purchase_id', 'POST', {'purchaseid':order['PurchaseID']})
	tracking.className = "text-center";
	tracking.innerText = shipment['TrackingNumber']
	let s = shipment['Status']
	status.className = "text-center";
	if (s == 0) {
	    status.innerText = "Preparing to ship";
	}
	else if (s == 1) {
	    status.innerText = "On the way";
	}
	else {
	    status.innerText = "Delivered";
	}


	orderRow.appendChild(orderDate);
	orderRow.appendChild(itemDetails);
	orderRow.appendChild(shippingAddress);
	orderRow.appendChild(payment);
	orderRow.appendChild(grandTotal);
	orderRow.appendChild(tracking);
	orderRow.appendChild(status);


	ordersTableBody.appendChild(orderRow);
    }

}

loadUserListings = function(){
    let user = JSON.parse(sessionStorage.getItem('user'));
    let itemList = makeApiCall('/items_by_user', 'POST', {'email': user['Email']});

    for (let i = 0; i < itemList.length; i++){
	let itemInfo = itemList[i];

	let itemRow = document.createElement('tr');
	let imageWrapper = document.createElement('td');
	let itemName = document.createElement('td');
	let quantity = document.createElement('td');
	let price = document.createElement('td');
	let delWrapper = document.createElement('td');

	let image = document.createElement('img');
	image.src = makeApiCall('/link_for_item', 'POST', {'id': itemInfo['ItemID']});
	image.style.width = '100px';
	imageWrapper.appendChild(image);

	itemName.innerText = itemInfo['Name'];
	quantity.innerText = itemInfo['Quantity'];
	price.innerText = itemInfo['Price'].toFixed(2);

	itemName.className = 'text-center';
	quantity.className = 'text-center';
	price.className = 'text-center';
	
	let deleteBtn = document.createElement('button');
	let deleteBtnX = document.createElement('span')
	deleteBtn.className = "close";
	deleteBtnX.innerHTML = "&times;";
	deleteBtn.appendChild(deleteBtnX);
	delWrapper.appendChild(deleteBtn);

	var deleteListing = function(itemRow, id, email){
	    
	    let res = makeApiCall('/delete_item_from_user', 'POST', {
		'email' : email,
		'id': id
	    });
	    if (res['success']){
		listingTableBody.removeChild(itemRow);
	    }
	}

	itemRow.appendChild(imageWrapper);
	itemRow.appendChild(itemName);
	itemRow.appendChild(quantity);
	itemRow.appendChild(price);
	itemRow.appendChild(delWrapper);
	
	listingTableBody.appendChild(itemRow);
	deleteBtn.addEventListener('click', function(e){
	    deleteListing(itemRow, itemInfo['ItemID'], user['Email']);
	});
    }
    
}

loadReviews = function(){
    let user = JSON.parse(sessionStorage.getItem('user'));
    let reviewsForUser = makeApiCall('reviews_for_user', 'POST', {'email': user['Email']});
    for (let i = 0; i < reviewsForUser.length; i++){
	let reviewInfo = reviewsForUser[i];
	let reviewRow = document.createElement('tr');
	let author = document.createElement('td');
	let rating = document.createElement('td');
	let comment = document.createElement('td');
	
	author.innerText = reviewInfo['BuyerEmail'];
	rating.innerText = reviewInfo['Score'];
	comment.innerText = reviewInfo['Feedback'];

	author.className = "text-center";
	rating.className = "text-center";
	comment.className = "text-center";
	
	reviewRow.appendChild(author);
	reviewRow.appendChild(rating);
	reviewRow.appendChild(comment);
	
	reviewsAsSellerTableBody.appendChild(reviewRow);

	
    }

    let reviewsByUser = makeApiCall('reviews_by_user', 'POST', {'email': user['Email']});
    for (let i = 0; i < reviewsByUser.length; i++){
	let reviewInfo = reviewsByUser[i];
	let reviewRow = document.createElement('tr');
	let recipient = document.createElement('td');
	let rating = document.createElement('td');
	let comment = document.createElement('td');
	
	recipient.innerText = reviewInfo['SellerEmail'];
	rating.innerText = reviewInfo['Score'];
	comment.innerText = reviewInfo['Feedback'];

	recipient.className = "text-center";
	rating.className = "text-center";
	comment.className = "text-center";
	
	reviewRow.appendChild(recipient);
	reviewRow.appendChild(rating);
	reviewRow.appendChild(comment);
	
	reviewsForOthersTableBody.appendChild(reviewRow);
    }

    
}

loadInfo();
loadOrders();
loadUserListings();
loadReviews();
updatePasswordBtn.addEventListener('click', update);
updateAddressBtn.addEventListener('click', update);
addCreditCardBtn.addEventListener('click', addCreditCard);
