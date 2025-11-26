// Función principal se ejecuta cuando el DOM está completamente cargado.
$(document).ready(function () {
  mostrarSaldoActual();
  cargarYMostrarContactos(); // Cargar contactos al iniciar
  agregarEventosBusqueda();
  agregarEventosFormularios();
  agregarEventosContactos();
  agregarEventosEdicion();
});

// Formatea un número como moneda en pesos chilenos (CLP) con separadores de miles.
function formatearPesos(monto) {
  const montoEntero = Math.round(monto);
  return montoEntero.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

// Muestra el saldo actual en el elemento correspondiente.
function mostrarSaldoActual() {
  const saldo = parseFloat(localStorage.getItem("saldo")) || 12500;
  $("#saldo-disponible").text(formatearPesos(saldo));
}

// Agrega los eventos para el formulario de búsqueda de contactos.
function agregarEventosBusqueda() {
  // Función para filtrar contactos
  function filtrarContactos() {
    const termino = $("#buscarContacto").val().toLowerCase().trim();

    if (!termino) {
      $("#lista-contactos .contact-card").show();
      return;
    }

    // Filtra contactos
    $("#lista-contactos .contact-card").each(function () {
      const nombre = $(this).data("nombre").toLowerCase();
      const alias = $(this).data("alias").toLowerCase();

      if (nombre.includes(termino) || alias.includes(termino)) {
        $(this).show();
      } else {
        $(this).hide();
      }
    });
  }

  // Prevenir el envío del formulario
  $("#searchForm").submit(function (event) {
    event.preventDefault();
    filtrarContactos();
  });

  // Filtrar en tiempo real mientras se escribe
  $("#buscarContacto").on("input", function () {
    filtrarContactos();
  });
}

// Agrega eventos para los formularios de agregar contacto y enviar dinero.
function agregarEventosFormularios() {
  // Modal para agregar contacto - resetea formulario al abrir
  $("#nuevoContactoModal").on("show.bs.modal", function () {
    $("#nuevoContactoForm")[0].reset();
  });

  // Validación en tiempo real del CBU (solo números) - Modal agregar
  $("#cbuContacto").on("input", function () {
    // Remueve cualquier carácter que no sea número
    this.value = this.value.replace(/\D/g, "");

    // Limita a 22 dígitos
    if (this.value.length > 22) {
      this.value = this.value.slice(0, 22);
    }
  });

  // Validación en tiempo real del CBU (solo números) - Modal editar
  $("#cbuContactoEditar").on("input", function () {
    // Remueve cualquier carácter que no sea número
    this.value = this.value.replace(/\D/g, "");

    // Limita a 22 dígitos
    if (this.value.length > 22) {
      this.value = this.value.slice(0, 22);
    }
  });

  // Guarda nuevo contacto
  $("#nuevoContactoModal .btn-success").click(function () {
    const nombre = $("#nombreContacto").val().trim();
    const cbu = $("#cbuContacto").val().trim();
    const alias = $("#aliasContacto").val().trim();
    const banco = $("#bancoContacto").val().trim();

    // Valida campos requeridos
    if (!nombre) {
      mostrarAlerta(
        "Por favor, ingresa el nombre y apellido del contacto.",
        "warning"
      );
      return;
    }

    // Valida CBU (debe tener 22 dígitos y solo números)
    if (!cbu || !/^\d{22}$/.test(cbu)) {
      mostrarAlerta(
        "Por favor, ingresa un número de CBU válido (22 dígitos numéricos).",
        "warning"
      );
      return;
    }

    if (!alias) {
      mostrarAlerta("Por favor, ingresa el alias.", "warning");
      return;
    }

    if (!banco) {
      mostrarAlerta("Por favor, ingresa el nombre del banco.", "warning");
      return;
    }

    // Guarda contacto
    const contacto = {
      nombre: nombre,
      cbu: cbu,
      alias: alias,
      banco: banco,
      fecha: new Date().toISOString(),
    };

    guardarContacto(contacto);

    mostrarAlerta(
      `¡Contacto agregado exitosamente! ${nombre} (${alias})`,
      "success"
    );

    // Cierra modal
    $("#nuevoContactoModal").modal("hide");

    // Limpia formulario
    $("#nuevoContactoForm")[0].reset();

    // Recarga lista de contactos
    cargarYMostrarContactos();
  });

  // Confirma el envío de dinero
  $("#enviarDineroModal .btn-success").click(function () {
    const monto = parseFloat($("#montoEnviar").val());
    const mensaje = $("#mensajeEnvio").val().trim();

    const contacto =
      $("#enviarDineroModal").data("contacto-nombre") || "Destinatario";

    // Valida monto
    if (isNaN(monto) || monto <= 0) {
      mostrarAlerta(
        "Por favor, ingresa un monto válido mayor a cero.",
        "warning"
      );
      return;
    }

    // Obtiene el saldo actual
    let saldoActual = parseFloat(localStorage.getItem("saldo")) || 12500;

    // Valida saldo
    if (monto > saldoActual) {
      mostrarAlerta(
        `Saldo insuficiente. Tu saldo actual es $${formatearPesos(
          saldoActual
        )}`,
        "danger"
      );
      return;
    }

    // Calcula nuevo saldo y redondea
    const nuevoSaldo = Math.round(saldoActual - monto);

    // Guarda nuevo saldo en localStorage
    localStorage.setItem("saldo", nuevoSaldo);

    // Guarda el movimiento en el historial
    guardarMovimiento({
      tipo: "envio",
      monto: monto,
      descripcion: `Envío a ${contacto}`,
      mensaje: mensaje,
      fecha: new Date().toISOString(),
    });

    // Muestra mensaje de confirmación usando jQuery
    mostrarMensajeConfirmacion(contacto, monto);

    // Cierra modal
    $("#enviarDineroModal").modal("hide");

    // Limpia formulario
    $("#enviarDineroForm")[0].reset();

    // Actualiza saldo
    mostrarSaldoActual();
  });
}

// Agrega los eventos de edición de contactos
function agregarEventosEdicion() {
  // Modal para editar contacto - resetea formulario al abrir
  $("#editarContactoModal").on("show.bs.modal", function () {
    $("#editarContactoForm")[0].reset();
  });

  // Evento para abrir modal de edición
  $(document).on("click", ".btn-editar-contacto", function (e) {
    e.stopPropagation();
    const cbu = $(this).data("cbu");
    const contacto = obtenerContactoPorCBU(cbu);

    if (contacto) {
      // Cargar datos en el formulario
      $("#cbuOriginal").val(contacto.cbu);
      $("#nombreContactoEditar").val(contacto.nombre);
      $("#cbuContactoEditar").val(contacto.cbu);
      $("#aliasContactoEditar").val(contacto.alias);
      $("#bancoContactoEditar").val(contacto.banco);
    }
  });

  // Guardar cambios del contacto editado
  $("#editarContactoModal .btn-success").click(function () {
    const cbuOriginal = $("#cbuOriginal").val();
    const nombre = $("#nombreContactoEditar").val().trim();
    const cbu = $("#cbuContactoEditar").val().trim();
    const alias = $("#aliasContactoEditar").val().trim();
    const banco = $("#bancoContactoEditar").val().trim();

    // Valida campos requeridos
    if (!nombre) {
      mostrarAlerta(
        "Por favor, ingresa el nombre y apellido del contacto.",
        "warning"
      );
      return;
    }

    // Valida CBU (debe tener 22 dígitos y solo números)
    if (!cbu || !/^\d{22}$/.test(cbu)) {
      mostrarAlerta(
        "Por favor, ingresa un número de CBU válido (22 dígitos numéricos).",
        "warning"
      );
      return;
    }

    if (!alias) {
      mostrarAlerta("Por favor, ingresa el alias.", "warning");
      return;
    }

    if (!banco) {
      mostrarAlerta("Por favor, ingresa el nombre del banco.", "warning");
      return;
    }

    // Actualiza el contacto
    const contactoActualizado = {
      nombre: nombre,
      cbu: cbu,
      alias: alias,
      banco: banco,
      fecha: new Date().toISOString(),
    };

    if (actualizarContacto(cbuOriginal, contactoActualizado)) {
      mostrarAlerta(
        `¡Contacto actualizado exitosamente! ${nombre} (${alias})`,
        "success"
      );

      // Cierra modal
      $("#editarContactoModal").modal("hide");

      // Limpia formulario
      $("#editarContactoForm")[0].reset();

      // Recarga lista de contactos
      cargarYMostrarContactos();
    } else {
      mostrarAlerta(
        "Error al actualizar el contacto. Por favor, intenta nuevamente.",
        "danger"
      );
    }
  });
}

// Agrega los eventos para las tarjetas de contacto.
function agregarEventosContactos() {
  $(document).on("click", ".btn-enviar-dinero", function () {
    const contacto = $(this).data("contacto");
    $("#enviarDineroModalLabel").text(`Enviar dinero a ${contacto}`);
    // Guarda el nombre del contacto en un data attribute del modal
    $("#enviarDineroModal").data("contacto-nombre", contacto);

    // Limpia formulario al abrir
    $("#enviarDineroForm")[0].reset();
  });

  // Evento para eliminar contacto
  $(document).on("click", ".btn-eliminar-contacto", function (e) {
    e.stopPropagation(); // Evita que se active el evento de selección del card
    const cbu = $(this).data("cbu");
    const nombre = $(this).data("nombre");

    // Confirma la eliminación
    if (
      confirm(
        `¿Estás seguro de que deseas eliminar a ${nombre} de tus contactos?`
      )
    ) {
      eliminarContacto(cbu);
      mostrarAlerta(`${nombre} ha sido eliminado de tus contactos.`, "success");
      cargarYMostrarContactos();
    }
  });

  // Delegación de eventos
  $(document).on("click", ".contact-card", function () {
    $(".contact-card").removeClass("active");
    $(this).addClass("active");
  });
}

// Muestra un mensaje de confirmación después de enviar dinero.
function mostrarMensajeConfirmacion(contacto, monto) {
  const mensaje = $("<div></div>")
    .addClass("alert alert-success alert-dismissible fade show")
    .attr("role", "alert").html(`
      <i class="bi bi-check-circle-fill me-2"></i>
      <strong>¡Envío exitoso!</strong> Has enviado $${formatearPesos(
        monto
      )} a ${contacto}.
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `);

  $("#mensaje-confirmacion").html(mensaje);

  // Auto-oculta después de 3 segundos
  setTimeout(function () {
    mensaje.alert("close");
  }, 3000);
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
          : "x-circle-fill"
      } me-2"></i>
      ${mensaje}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `);

  $("#alert-container").html(alerta);

  // Auto-oculta la alerta después de 3 segundos
  setTimeout(function () {
    alerta.alert("close");
  }, 3000);
}

// Guarda un contacto en el localStorage.
function guardarContacto(contacto) {
  // Obtiene lista de contactos existentes o crea array vacío
  let contactos = JSON.parse(localStorage.getItem("contactos")) || [];
  contactos.unshift(contacto);
  localStorage.setItem("contactos", JSON.stringify(contactos));
}

// Elimina un contacto del localStorage por su CBU
function eliminarContacto(cbu) {
  let contactos = JSON.parse(localStorage.getItem("contactos")) || [];
  // Filtra el array para eliminar el contacto con el CBU especificado
  contactos = contactos.filter((contacto) => contacto.cbu !== cbu);
  localStorage.setItem("contactos", JSON.stringify(contactos));
}

// Obtiene un contacto específico por su CBU
function obtenerContactoPorCBU(cbu) {
  const contactos = JSON.parse(localStorage.getItem("contactos")) || [];
  return contactos.find((contacto) => contacto.cbu === cbu);
}

// Actualiza un contacto existente en el localStorage
function actualizarContacto(cbuOriginal, contactoActualizado) {
  let contactos = JSON.parse(localStorage.getItem("contactos")) || [];
  const index = contactos.findIndex((contacto) => contacto.cbu === cbuOriginal);

  if (index !== -1) {
    contactos[index] = contactoActualizado;
    localStorage.setItem("contactos", JSON.stringify(contactos));
    return true;
  }
  return false;
}

// Carga los contactos desde localStorage.
function cargarContactos() {
  let contactos = JSON.parse(localStorage.getItem("contactos")) || [];

  // Si no hay contactos, crea uno hardcodeado
  if (contactos.length === 0) {
    const contactoDefault = {
      nombre: "Elon Musk",
      cbu: "1234567890123456789999",
      alias: "elon.musk.spacex",
      banco: "Banco Tesla",
      fecha: new Date().toISOString(),
    };
    contactos.push(contactoDefault);
    localStorage.setItem("contactos", JSON.stringify(contactos));
  }

  console.log(`Contactos cargados: ${contactos.length}`);
  return contactos;
}

// Carga y muestra todos los contactos en la lista
function cargarYMostrarContactos() {
  const contactos = cargarContactos();
  const listaContactos = $("#lista-contactos");

  // Limpia la lista actual
  listaContactos.empty();

  if (contactos.length === 0) {
    listaContactos.html(`
      <div class="text-center py-4">
        <i class="bi bi-person-x empty-state-icon"></i>
        <p class="text-muted mt-2">No hay contactos guardados</p>
        <small class="text-muted">Agrega tu primer contacto usando el botón de arriba</small>
      </div>
    `);
    return;
  }

  // Agrega cada contacto a la lista
  contactos.forEach(function (contacto) {
    const contactCard = `
      <div class="contact-card" data-nombre="${contacto.nombre}" data-alias="${contacto.alias}" data-cbu="${contacto.cbu}">
        <div class="d-flex justify-content-between align-items-center">
          <div class="d-flex align-items-center">
            <div class="contact-avatar me-3">
              <i class="bi bi-person-fill"></i>
            </div>
            <div>
              <h6 class="mb-1 fw-bold">${contacto.nombre}</h6>
              <small>${contacto.alias}</small>
            </div>
          </div>
          <div class="d-flex gap-2">
            <button class="btn btn-sm btn-menu btn-enviar-dinero" data-bs-toggle="modal"
              data-bs-target="#enviarDineroModal" data-contacto="${contacto.nombre}">
              <i class="bi bi-send"></i>
            </button>
            <button class="btn btn-sm btn-primary btn-editar-contacto" data-bs-toggle="modal"
              data-bs-target="#editarContactoModal" data-cbu="${contacto.cbu}">
              <i class="bi bi-pencil"></i>
            </button>
            <button class="btn btn-sm btn-danger btn-eliminar-contacto" data-cbu="${contacto.cbu}" data-nombre="${contacto.nombre}">
              <i class="bi bi-trash"></i>
            </button>
          </div>
        </div>
      </div>
    `;
    listaContactos.append(contactCard);
  });
}

// Guarda un movimiento en el historial de transacciones en localStorage
function guardarMovimiento(movimiento) {
  // Obtiene movimientos desde localStorage o crea array vacío
  let movimientos = JSON.parse(localStorage.getItem("movimientos")) || [];
  movimientos.unshift(movimiento);
  localStorage.setItem("movimientos", JSON.stringify(movimientos));
}
