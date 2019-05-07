var accountLink = document.getElementById('account');
var cartLink = document.getElementById('cart');
var registerLink = document.getElementById('signUp');
var loginLink = document.getElementById('logIn');
var postListingLink = document.getElementById('postListing');

var userName = document.getElementById('name');
var email = document.getElementById('email');
var rating = document.getElementById('rating');
var dateJoined = document.getElementById('dateJoined');

var searchWrapper = document.getElementById('searchWrapper');
var search = document.getElementById('search');

var infoContainer = document.getElementById('infoContainer');
var reviewsTableBody = document.getElementById('reviewsTableBody');
var reviewText = document.getElementById('reviewText');
var reviewSubmit = document.getElementById('reviewSubmit');
var score = document.getElementById('score');

var currentResult = null;

loadLinks = function(){
    if (sessionStorage.getItem('user') != null){
	registerLink.className = 'nav-link not-displayed';
	loginLink.className = 'nav-link not-displayed';
    }else{
	accountLink.className = 'nav-link not-displayed';
	cartLink.className = 'nav-link not-displayed';
	postListingLink.className = 'nav-link not-displayed';

    }
}

searchSeller = function(searchQuery){
    reviewsTableBody.innerHTML = "";
    let userList = makeApiCall('/users', 'GET', null);
    for (let i = 0; i < userList.length; i++){
	let userInfo = userList[i];
	if (userInfo['Email'] == searchQuery.trim()){
	    currentResult = userInfo;
	    let infoContainer = document.getElementById('infoContainer');
	    infoContainer.className = "container w-50 mt-5";

	    if (sessionStorage.getItem('user') != null){
		let reviewForm = document.getElementById('reviewForm');
		reviewForm.className = "form-group container w-50 text-center";
	    }
	    
	    
	    userName.innerText = userInfo['FirstName'] + ' ' + userInfo['LastName'];
	    email.innerText = userInfo['Email'];
	    rating.innerText = userInfo['Rating'];
	    dateJoined.innerText = userInfo['DateJoined'];

	    let reviewsList = makeApiCall('/reviews_for_user', 'POST', {'email': userInfo['Email']});

	    if (reviewsList.length > 0){
		let reviewsContainer = document.getElementById('reviewsContainer');
		let reviewsTable = document.getElementById('reviewsTable');
		reviewsContainer.className = "container text-center mt-5";
		reviewsTable.className = "table table-striped col-8 mt-5";
	    }
	    
	    for (let j = 0; j < reviewsList.length; j++){
		let reviewInfo = reviewsList[j];
		let reviewRow = document.createElement('tr');
		let author = document.createElement('td');
		let comment = document.createElement('td');

		author.innerText = reviewInfo['BuyerEmail'];
		comment.innerText = reviewInfo['Feedback'];

		reviewRow.appendChild(author);
		reviewRow.appendChild(comment);

		reviewsTableBody.appendChild(reviewRow);
	    }
	    break;
	}
    }
}

leaveReview = function(){
    let user = JSON.parse(sessionStorage.getItem('user'));
    let reviewParams = {
	'buyer_email': user['Email'],
	'seller_email': currentResult['Email'],
	'item_name': 'placeholder',
	'feedback': reviewText.value,
	'score': parseInt(score.value)
	
    };
    
    let res = makeApiCall('/make_review', 'POST', reviewParams);
    reviewText.value = "";
    searchSeller(currentResult['Email']);
}

loadLinks();
search.addEventListener('keyup', function(e){
    if (e.keyCode == 13){
	e.preventDefault();

	let searchQuery = search.value;
	search.value = "";
	searchSeller(searchQuery);
	
    }
});

reviewSubmit.addEventListener('click', leaveReview);
