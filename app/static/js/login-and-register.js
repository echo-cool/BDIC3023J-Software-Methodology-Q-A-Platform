
var signUpButton = document.getElementById('signUp')
var signInButton = document.getElementById('signIn')
var container = document.getElementById('mainbox')

signUpButton.addEventListener('click', function () {
    container.classList.add('right-panel-active')
})

signInButton.addEventListener('click', function () {
    container.classList.remove('right-panel-active')
});

function check_email(str){
　	var pattern = new RegExp("@");
	var email = document.getElementById("email");
　	if (pattern.test(str.value)){
　　}
	else{
		alert("Please enter correct email address！")
		email.focus();
	}
}