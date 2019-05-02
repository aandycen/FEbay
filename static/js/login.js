var email = document.getElementById('email');
var password = document.getElementById('password');
var loginBtn = document.getElementById('loginBtn');
var loginStatus = document.getElementById("loginStatus");

loginUser = function(){
    params = { 
	       'email': email.value,
	       'password': password.value,
	     };

    var res = makeApiCall('/login', 'POST', params);

    loginStatus.innerText = res['success']? 'Success' : res['error'];

    if (loginStatus.innerText == 'Success'){
	
	res = makeApiCall('/profile', 'POST', {'email': email.value})
	sessionStorage.setItem('user', JSON.stringify(res));
	redirect('/');
    }
    
}

loginBtn.addEventListener('click', loginUser);
