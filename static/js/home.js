
var accountBtn = document.getElementById('accountBtn');

toAccountPage = function(){
    redirect('/account');
    
}

loadLinks = function(){
    accountBtn.style.display = 'none';
    if (sessionStorage.getItem('user') != null){
	accountBtn.style.display = 'block';
    }
}
loadLinks();
accountBtn.addEventListener('click', toAccountPage);
