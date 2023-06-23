
// password variables
const inputPassword = document.querySelector('#pwd');
const showPassword = document.querySelector('#showpwd');

// page loader
let loading = document.querySelector('#page');


loadAllFunction();
function loadAllFunction() {
    window.addEventListener('load', loads);
    showPassword.addEventListener('click', showMyPassword);
}
// view password
function showMyPassword(e) {
    if (inputPassword.type === 'password') {
        inputPassword.type = 'text'
    } else {
        inputPassword.type = 'password'
    }
    e.preventDefault();
}

// loader
function loads() {
    setTimeout(() => {
        loading.classList.add('loader')
    }, 2000)
}



