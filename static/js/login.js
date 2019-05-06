var email = document.getElementById('email');
var password = document.getElementById('password');
var loginBtn = document.getElementById('loginBtn');
var loginStatus = document.getElementById("loginStatus");
var snackbar = document.getElementById('snackbar');

errorAlert = function() {
    var x = document.getElementById("snackbar");
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

loginUser = function(){
    params = { 
    	'email': email.value,
		'password': password.value,
	};

    var res = makeApiCall('/login', 'POST', params);

    snackbar.innerText = res['error'];

    if (res['success']){
		res = makeApiCall('/account', 'POST', {'email': email.value})
		sessionStorage.setItem('user', JSON.stringify(res));
		redirect('/');
    }
    else {
        errorAlert();
    }
}

loginBtn.addEventListener('click', loginUser);
