var itemName = document.getElementById('itemName');
var quantity = document.getElementById('quantity');
var pricePerUnit = document.getElementById('pricePerUnit');
var photo = document.getElementById('photo');

var postListingBtn = document.getElementById('postListingBtn');
var postlistingStatus = document.getElementById('postListingStatus');
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
	postListingStatus.innerText = res['message'];
    }else{
	postListingStatus.innerText = res['error'];
    }
    
}

postListingBtn.addEventListener('click', postItem);
