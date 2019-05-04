email = document.getElementById('email');
password = document.getElementById('password');
firstname = document.getElementById('firstname');
lastname = document.getElementById('lastname');
registerBtn = document.getElementById('registerBtn');
registerStatus = document.getElementById('registerStatus');

registerUser = function() {
	params = {
		'first': firstname.value,
		'last': lastname.value,
		'email': email.value,
		'password': password.value
	};

    var res = makeApiCall('/register', 'POST', params);
    
    registerStatus.innerText = res['error'];
    if (res['success']) {
    	redirect('/');
    }
}

registerBtn.addEventListener('click', registerUser);
