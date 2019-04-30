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
    console.log(res);
    console.log(res['error']);
    loginStatus.innerText = res['success']? 'Success' : res['error'];

    if (loginStatus.innerText == 'Success'){
	
	res = makeApiCall('/user_info', 'POST', {'email': email.value})
	localStorage.setItem('user', JSON.stringify(res));
    }
    
}

loginBtn.addEventListener('click', loginUser);
