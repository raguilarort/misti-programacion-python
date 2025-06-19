document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const errorMessageDiv = document.getElementById('errorMessage');

    // Función para alternar la visibilidad de la contraseña
    window.togglePasswordVisibility = function() {
        const passwordField = document.getElementById('password');
        const toggleIcon = document.querySelector('.password-toggle');
        if (passwordField.type === 'password') {
            passwordField.type = 'text';
            toggleIcon.innerHTML = '&#128064;'; // Ojo abierto
        } else {
            passwordField.type = 'password';
            toggleIcon.innerHTML = '&#128065;'; // Ojo cerrado
        }
    };

    // Ejemplo de validación del lado del cliente (puedes expandirlo)
    loginForm.addEventListener('submit', function(event) {
        // En Django, la validación principal debe ser del lado del servidor.
        // Aquí puedes agregar validaciones básicas antes de enviar el formulario.
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        if (username.trim() === '' || password.trim() === '') {
            errorMessageDiv.textContent = 'Por favor, ingresa tu usuario y contraseña.';
            event.preventDefault(); // Previene el envío del formulario si hay errores
        } else {
            errorMessageDiv.textContent = ''; // Limpia el mensaje de error
            // Aquí, en un entorno real de Django, el formulario se enviaría al servidor.
            // La respuesta del servidor (éxito o error) se manejaría luego.
        }
    });

    // En un entorno de Django, si el servidor devuelve un error de autenticación,
    // puedes pasarlo al template y mostrarlo aquí. Por ejemplo:
    // {% if form.errors %}
    //     <script>
    //         document.getElementById('errorMessage').textContent = '{{ form.errors.non_field_errors.0 }}';
    //     </script>
    // {% endif %}
});