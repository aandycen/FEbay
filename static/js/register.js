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
	res = makeApiCall('/login', 'POST', {'email': params['email'],
					     'password' : params['password']
					    });
	sessionStorage.setItem('user', JSON.stringify(res));
	redirect('/');
    }
}

registerBtn.addEventListener('click', registerUser);
