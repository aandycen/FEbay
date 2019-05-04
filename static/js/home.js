var profileBtn = document.getElementById('accountBtn');

loadLinks = function(){
    profileBtn.style.display = 'none';
    if (sessionStorage.getItem('user') != null){
	profileBtn.style.display = 'block';
    }
}
loadLinks();