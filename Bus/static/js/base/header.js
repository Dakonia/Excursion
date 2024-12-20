const LoginModal = document.getElementById('modal-login');
const ExitLogin = document.getElementById('exit-login-modal');
const LoginBut = document.getElementById('but-login');
const LoginButton = document.getElementById('login-button'); 
const LoginForm = document.getElementById('login-form'); 
const ErrorMessage = document.getElementById('error-message'); 


LoginBut.addEventListener('click', function () {
    LoginModal.style.display = 'flex';
    console.log('Открыто модальное окно');
});


ExitLogin.addEventListener('click', function () {
    LoginModal.style.display = 'none';
    LoginForm.reset(); 
    ErrorMessage.style.display = 'none'; 
    console.log('Модальное окно закрыто');
});


function submitLoginForm() {
    const formData = new FormData(LoginForm);

    fetch('/', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest', 
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        },
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка сети');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url;
            } else {

                ErrorMessage.textContent = data.error || 'Неизвестная ошибка.';
                ErrorMessage.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            ErrorMessage.textContent = 'Ошибка сервера. Повторите попытку позже.';
            ErrorMessage.style.display = 'block';
        });
}

LoginButton.addEventListener('click', function (event) {
    event.preventDefault(); 
    submitLoginForm();
});


LoginForm.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault(); 
        submitLoginForm(); 
    }
});
