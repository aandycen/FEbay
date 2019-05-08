var shippingAddress = document.getElementById('shippingAddress');
var billingAddress = document.getElementById('billingAddress');

var CCN = document.getElementById('CCN');
var expireDate = document.getElementById('expireDate');
var securityCode = document.getElementById('securityCode');

var USPS = document.getElementById('USPS');
var FedEx = document.getElementById('Fedex');

var ccDropdown = document.getElementById('ccDropdown');

var grandTotal = document.getElementById('grandTotal');
var checkoutBtn = document.getElementById('checkoutBtn');

autofill = function(){
    let user = JSON.parse(sessionStorage.getItem('user'));
    shippingAddress.value = user['Shipping'];
    billingAddress.value = user['Billing'];
    grandTotal.firstChild.innerText += " $" + makeApiCall('get_shopping_cart', 'POST', {'email': user['Email']})['total'].toFixed(2);
}

/*
<li role="presentation" class="text-center"><a role="menuitem" tabindex="-1" href="#">1111111111111111</a></li>
			            		<div class="dropdown-divider"></div>
*/


loadCreditCardOptions = function(){
    let user = JSON.parse(sessionStorage.getItem('user'));
    let userEmail = user['Email'];

    let res = makeApiCall('/cards_from_user', 'POST', {'email': userEmail});
    for (let i = 0; i < res.length; i++){
	let card = res[i];
	let cardOption = document.createElement('li');
	cardOption.className = 'text-center';
	let cardOptionLink = document.createElement('a');
	cardOptionLink.role = 'menuitem';
	cardOptionLink.tabindex = '-1';
	cardOptionLink.href = '#';
	cardOptionLink.innerText = card['CCN'];
	cardOption.appendChild(cardOptionLink);

	var autofillCC = function(cardInfo){
	    CCN.value = cardInfo['CCN'];
	    expireDate.value = cardInfo['ExpiryDate'];
	    securityCode.value = cardInfo['SecurityCode'];

	};

	cardOption.addEventListener('click', function(e){
	    e.preventDefault();
	    autofillCC(card);
	});

	let divider = document.createElement('div');
	divider.className = 'dropdown-divider';

	ccDropdown.appendChild(cardOption);
	ccDropdown.appendChild(divider);

    }
}

checkout = function(){
    let user = JSON.parse(sessionStorage.getItem('user'));
    let facility = FedEx.checked? 'FedEx': 'USPS';
    let checkoutParams = {
	'email': user['Email'],
	'ccn': CCN.value,
  'expirydate': expireDate.value,
  'securitycode': securityCode.value,
	'billing': billingAddress.value,
	'shipping': shippingAddress.value,
	'facility': facility
    };

    let updateCCParams = {
	'email': user['Email'],
	'info': 'creditcard',
	'action': 'add',
	'ccn': CCN.value,
	'securitycode' : securityCode.value,
    	'expirydate' : expireDate.value
    };

    let updateShippingParams = {
    	'info' : 'shipping',
    	'address' : shippingAddress.value,
    	'email' : user['Email']
    }
    let updateBillingParams = {
    	'info' : 'billing',
    	'address' : billingAddress.value,
    	'email' : user['Email']
    }
    //makeApiCall('/update_info', 'POST', updateCCParams);
    //makeApiCall('/update_info', 'POST', updateShippingParams);
    //makeApiCall('/update_info', 'POST', updateBillingParams);

    let res = makeApiCall('/checkout_cart', 'POST', checkoutParams);
    if (res['success']) {
      redirect('/');
    }
    console.log(res);
}

autofill();
loadCreditCardOptions();

checkoutBtn.addEventListener('click', checkout);
