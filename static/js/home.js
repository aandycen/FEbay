
var profileBtn = document.getElementById('accountBtn');

toAccountPage = function(){
    redirect('/profile');
    
}

loadLinks = function(){
    profileBtn.style.display = 'none';
    if (sessionStorage.getItem('user') != null){
	profileBtn.style.display = 'block';
    }
}
loadLinks();
profileBtn.addEventListener('click', toAccountPage);