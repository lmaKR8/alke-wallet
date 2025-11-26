// Función principal se ejecuta cuando el DOM está completamente cargado.
$(document).ready(function () {
  mostrarSaldoActual();

  // Maneja el envío del formulario de depósito
  $("#depositForm").submit(function (event) {
    event.preventDefault();

    const monto = parseFloat($("#monto").val());

    // Valida el monto
    if (isNaN(monto) || monto <= 0) {
      mostrarAlerta(
        "Por favor, ingresa un monto válido mayor a cero.",
        "warning"
      );
      $("#monto").focus();
      return;
    }

    // Obtiene el saldo actual de localStorage o usa valor por defecto
    let saldoActual = parseFloat(localStorage.getItem("saldo"));
    if (isNaN(saldoActual)) {
      saldoActual = 12500;
    }

    // Calcula nuevo saldo redondeado
    const nuevoSaldo = Math.round(saldoActual + monto);

    // Guarda nuevo saldo en localStorage
    localStorage.setItem("saldo", nuevoSaldo);

    // Guarda el movimiento en el historial
    guardarMovimiento({
      tipo: "deposito",
      monto: monto,
      descripcion: "Depósito recibido",
      fecha: new Date().toISOString(),
    });

    // Muestra monto depositado
    mostrarLeyendaDeposito(monto);

    mostrarAlerta(
      `¡Depósito exitoso! Monto depositado: $${formatearPesos(
        monto
      )}. Nuevo saldo: $${formatearPesos(nuevoSaldo)}`,
      "success"
    );

    // Redirige al menú después de 3 segundos
    setTimeout(function () {
      window.location.href = "menu.html";
    }, 3000);
  });
});

// Formatea un número como moneda en pesos chilenos (CLP) con separadores de miles.
function formatearPesos(monto) {
  const montoEntero = Math.round(monto);
  return montoEntero.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

// Muestra el saldo actual en la interfaz
function mostrarSaldoActual() {
  const saldo = parseFloat(localStorage.getItem("saldo")) || 12500;

  $("#saldo-actual").text(`$${formatearPesos(saldo)}`);
}

// Muestra una leyenda con el monto depositado
function mostrarLeyendaDeposito(monto) {
  const leyenda = $("<div></div>").addClass("alert alert-success mt-3").html(`
      <i class="bi bi-check-circle-fill me-2"></i>
      <strong>Monto depositado:</strong> $${formatearPesos(monto)}
    `);

  $("#deposito-info").html(leyenda);
}

// Muestra una alerta en la parte superior del formulario
function mostrarAlerta(mensaje, tipo) {
  const alerta = $("<div></div>")
    .addClass(`alert alert-${tipo} alert-dismissible fade show`)
    .attr("role", "alert").html(`
      <i class="bi bi-${
        tipo === "success"
          ? "check-circle-fill"
          : tipo === "warning"
          ? "exclamation-triangle-fill"
          : "info-circle-fill"
      } me-2"></i>
      ${mensaje}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `);

  // Limpia alertas anteriores y agrega la nueva
  $("#alert-container").html(alerta);

  // Auto-oculta la alerta después de 3 segundos
  setTimeout(function () {
    alerta.alert("close");
  }, 3000);
}

// Guarda un movimiento en el historial de transacciones en localStorage
function guardarMovimiento(movimiento) {
  // Obtiene movimientos existentes desde localStorage o crea array vacío
  let movimientos = JSON.parse(localStorage.getItem("movimientos")) || [];

  // Agrega el nuevo movimiento al inicio del array
  movimientos.unshift(movimiento);

  // Guarda en localStorage
  localStorage.setItem("movimientos", JSON.stringify(movimientos));
}
