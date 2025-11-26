// Credenciales válidas para simulación de inicio de sesión
const CREDENCIALES_VALIDAS = {
  email: "usuario@ejemplo.com",
  password: "12345",
};

// Función principal se ejecuta cuando el DOM está completamente cargado.
$(document).ready(function () {
  // Maneja el envío del formulario de inicio de sesión
  $("#loginForm").submit(function (event) {
    event.preventDefault();

    const email = $("#email").val();
    const password = $("#password").val();

    // Validación de credenciales
    if (
      email === CREDENCIALES_VALIDAS.email &&
      password === CREDENCIALES_VALIDAS.password
    ) {
      mostrarAlerta(
        "¡Inicio de sesión exitoso! Bienvenido a tu billetera digital.",
        "success"
      );

      // Redirige al menu después de 2 segundos
      setTimeout(function () {
        window.location.href = "menu.html";
      }, 2000);
    } else {
      mostrarAlerta(
        "Error: Email o contraseña incorrectos. Por favor, intenta nuevamente.",
        "danger"
      );

      // Limpia la contraseña y enfoca en el email
      $("#password").val("");
      $("#email").focus();
    }
  });
});

// Función para mostrar alertas dinámicas
function mostrarAlerta(mensaje, tipo) {
  const alerta = $("<div></div>")
    .addClass(`alert alert-${tipo} alert-dismissible fade show`)
    .attr("role", "alert").html(`
      <i class="bi bi-${
        tipo === "success" ? "check-circle-fill" : "exclamation-triangle-fill"
      } me-2"></i>
      ${mensaje}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `);

  // Limpia alertas anteriores y agrega la nueva
  $("#alert-container").empty().append(alerta);

  // Auto-oculta la alerta después de 2 segundos
  setTimeout(function () {
    alerta.alert("close");
  }, 2000);
}
