email = document.getElementById('email');
password = document.getElementById('password');
loginBtn = document.getElementById('loginBtn');
loginStatus = document.getElementById("loginStatus");

loginUser = function(){
    params = { 
	       'email': email.value,
	       'password': password.value,
	     };

    var res = makeApiCall('/login', 'POST', params);
    
    loginStatus.innerText = res['success']? 'Success' : res['error'];
    
}

loginBtn.addEventListener('click', loginUser);
