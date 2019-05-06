email = document.getElementById('email');
password = document.getElementById('password');
firstname = document.getElementById('firstname');
lastname = document.getElementById('lastname');
registerBtn = document.getElementById('registerBtn');
registerStatus = document.getElementById('registerStatus');
snackbar = document.getElementById('snackbar');

errorAlert = function() {
	var x = document.getElementById("snackbar");
	x.className = "show";
	setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

registerUser = function() {
	params = {
		'first': firstname.value,
		'last': lastname.value,
		'email': email.value,
		'password': password.value
	};

    var res = makeApiCall('/register', 'POST', params);
    
    //registerStatus.innerText = res['error'];
    snackbar.innerText = res['error'];
    if (res['success']) {
	res = makeApiCall('/login', 'POST', {'email': params['email'],
					     'password' : params['password']
					    });
	res = makeApiCall('/account', 'POST', {'email': params['email']});
	sessionStorage.setItem('user', JSON.stringify(res));
	redirect('/');
    }
    else {
    	errorAlert();
    }
}

registerBtn.addEventListener('click', registerUser);
