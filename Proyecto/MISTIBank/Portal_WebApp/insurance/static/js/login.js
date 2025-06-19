document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const errorMessageDiv = document.getElementById('errorMessage');

    // Alternar visibilidad de la contraseña
    window.togglePasswordVisibility = function() {
        const passwordField = document.getElementById('password');
        const toggleIcon = document.querySelector('.password-toggle');
        if (passwordField.type === 'password') {
            passwordField.type = 'text';
            toggleIcon.innerHTML = '🙈'; // Cambiar ícono a ojo cerrado
        } else {
            passwordField.type = 'password';
            toggleIcon.innerHTML = '👁️'; // Cambiar ícono a ojo abierto
        }
    };

    // Validación básica del formulario
    loginForm.addEventListener('submit', function(event) {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        if (username.trim() === '' || password.trim() === '') {
            errorMessageDiv.textContent = 'Por favor, ingresa tu usuario y contraseña.';
            event.preventDefault(); // Detiene el envío si hay error
        } else {
            errorMessageDiv.textContent = '';
        }
    });
});
