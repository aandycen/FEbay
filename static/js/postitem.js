var itemName = document.getElementById('itemName');
var quantity = document.getElementById('quantity');
var pricePerUnit = document.getElementById('pricePerUnit');
var photo = document.getElementById('photo');

var postListingBtn = document.getElementById('postListingBtn');
var snackbar = document.getElementById('snackbar');
var logOutLink = document.getElementById('logOut');

logOutLink.onclick = function(event){
    event.preventDefault();
    console.log("Prevented Default Action");
    sessionStorage.clear();
    redirect('/');
}

errorAlert = function() {
	var x = document.getElementById("snackbar");
	x.className = "show";
	setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

postItem = function(){
    let user = JSON.parse(sessionStorage.getItem('user'));
    params = {
	'email': user['Email'],
	'price': parseFloat(pricePerUnit.value),
	'quantity': parseInt(quantity.value),
	'name': itemName.value,
	'link': photo.value
    };
    let res = makeApiCall('/add_item', 'POST', params);
    if (res['success']){
    	snackbar.innerText = res['message'];
		errorAlert();
		redirect("/");
    }
    else {
		snackbar.innerText = res['error'];
		errorAlert();
    }
    
}

postListingBtn.addEventListener('click', postItem);
