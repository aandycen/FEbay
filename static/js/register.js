email = document.getElementById('email');
password = document.getElementById('password');
firstname = document.getElementById('firstname');
lastname = document.getElementById('lastname');
registerBtn = document.getElementById('registerBtn');
status = document.getElementById("status");

registerUser = function(){
    params = { 'firstname': firstname.value,
	       'lastname': lastname.value,
	       'email': email.value,
	       'password': password.value,
	       
	
	     };
    
    status.innerText = makeApiCall('/register', 'POST', params);
    
}

registerBtn.addEventListener('click', registerUser);
