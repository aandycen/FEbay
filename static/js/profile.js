
var updateBtn = document.getElementById('updateBtn');
var updateBtn = document.getElementById('updateBtn');
var shippingAddress = document.getElementById('shippingAddress');
var billingAddress = document.getElementById('billingAddress');
var password = document.getElementById('password');

update = function(){
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

    let res = makeApiCall('/profile', 'POST', {'email': user['Email']})
    sessionStorage.setItem('user', JSON.stringify(res));
}

loadInfo = function(){
    let user = JSON.parse(sessionStorage.getItem('user'));
    if (user['Shipping'] != null){
	shippingAddress.value = user['Shipping'];
    }
    if (user['Billing'] != null){
	billingAddress.value = user['Billing'];
    }
    password.value = user['Password'];
    
}


loadInfo();
updateBtn.addEventListener('click', update);
