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
    password = {
    	'info' : 'password',
    	'password' : password.value,
    	'email' : user['Email']
    }

    makeApiCall('/update_info', 'POST', shipping);
    makeApiCall('/update_info', 'POST', billing);
    makeApiCall('/update_info', 'POST', password);

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
    console.log(res);
    if (res['success']){
	       addCreditCardHTML(CCN.value, expiryDate.value, securityCode.value);
    }
    creditCardStatus.innerText = res['message'];


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
	let billingAddress = document.createElement('td');
  let payment = document.createElement('td');


  orderDate.innerText = order['OrderDate'].split(" ")[0];
  itemText = "";
  for (let i = 0; i < order['Items'].length; i++) {
    itemText += order['Items'][i]['item'] + " : " + order['Items'][i]['quantity'] + " : " + order['Items'][i]['seller'] + "\n";
  }
  itemDetails.innerText = itemText;
  shippingAddress.innerText = order['Shipping'];
  billingAddress.innerText = order['Billing'];
  payment.innerText = "$" + order['Price'];


	orderRow.appendChild(orderDate);
	orderRow.appendChild(itemDetails);
	orderRow.appendChild(shippingAddress);
	orderRow.appendChild(billingAddress);
	orderRow.appendChild(payment);


	ordersTableBody.appendChild(orderRow);
    }

}

loadInfo();
loadOrders();

updatePasswordBtn.addEventListener('click', update);
updateAddressBtn.addEventListener('click', update);
addCreditCardBtn.addEventListener('click', addCreditCard);
