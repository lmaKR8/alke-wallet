// Función principal se ejecuta cuando el DOM está completamente cargado.
$(document).ready(function () {
  cargarSaldo();
  agregarEventosBotones();
});

// Formatea un número como monto en pesos chilenos con separadores de miles.
function formatearPesos(monto) {
  const montoEntero = Math.round(monto);
  return montoEntero.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

// Carga el saldo desde el almacenamiento local y lo muestra en la interfaz.
function cargarSaldo() {
  let saldo = parseFloat(localStorage.getItem("saldo"));

  // Si no existe saldo válido, inicializa con el valor por defecto
  if (isNaN(saldo) || saldo === null) {
    saldo = 12500;
    localStorage.setItem("saldo", saldo);
  }

  // Formatea y muestra el saldo
  $("#saldo").text("$" + formatearPesos(saldo));
}

// Agrega eventos de clic a los botones del menú para mostrar mensajes de redirección.
function agregarEventosBotones() {
  // Botón Depositar
  $('a[href="deposit.html"]').on("click", function (event) {
    event.preventDefault();
    mostrarMensajeRedireccion("Depositar");
    setTimeout(function () {
      window.location.href = "deposit.html";
    }, 1000);
  });

  // Botón Enviar Dinero
  $('a[href="sendMoney.html"]').on("click", function (event) {
    event.preventDefault();
    mostrarMensajeRedireccion("Enviar Dinero");
    setTimeout(function () {
      window.location.href = "sendMoney.html";
    }, 1000);
  });

  // Botón Últimos Movimientos
  $('a[href="transactions.html"]').on("click", function (event) {
    event.preventDefault();
    mostrarMensajeRedireccion("Últimos Movimientos");
    setTimeout(function () {
      window.location.href = "transactions.html";
    }, 1000);
  });
}

// Muestra un mensaje de redirección utilizando un toast de Bootstrap.
function mostrarMensajeRedireccion(nombrePantalla) {
  // Crea un toast de Bootstrap
  const toastHtml = `
    <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 11">
      <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header bg-success text-white">
          <i class="bi bi-arrow-right-circle-fill me-2"></i>
          <strong class="me-auto">Redirigiendo</strong>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
          Redirigiendo a ${nombrePantalla}...
        </div>
      </div>
    </div>
  `;

  // Agrega al body
  $("body").append(toastHtml);

  // Remueve después de 3 segundos
  setTimeout(function () {
    $(".toast").remove();
  }, 3000);
}
