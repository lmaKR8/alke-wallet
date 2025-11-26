// Función principal se ejecuta cuando el DOM está completamente cargado.
$(document).ready(function () {
  cargarMovimientos();
  agregarEventosFiltros();
  agregarEventosPaginacion();
});

// Variable global para la paginación
let paginaActual = 1;
const itemsPorPagina = 5;
let movimientosFiltrados = [];

// Formatea un número como moneda en pesos chilenos (CLP) con separadores de miles.
function formatearPesos(monto) {
  const montoEntero = Math.round(monto);
  return montoEntero.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

// Agrega eventos a los filtros de tipo y período.
function agregarEventosFiltros() {
  // Evento para filtro de tipo
  $("#filtroTipo").change(function () {
    aplicarFiltros();
  });

  // Evento para filtro de período
  $("#filtroPeriodo").change(function () {
    aplicarFiltros();
  });
}

// Aplica los filtros seleccionados y actualiza la lista de movimientos.
function aplicarFiltros() {
  const tipoSeleccionado = $("#filtroTipo").val();
  const periodoSeleccionado = parseInt($("#filtroPeriodo").val());

  // Obtiene movimientos desde localStorage
  let movimientos = JSON.parse(localStorage.getItem("movimientos")) || [];

  // Filtra por tipo
  if (tipoSeleccionado !== "todos") {
    movimientos = movimientos.filter(function (mov) {
      return mov.tipo === tipoSeleccionado;
    });
  }

  // Filtra por período
  const fechaLimite = new Date();
  fechaLimite.setDate(fechaLimite.getDate() - periodoSeleccionado);

  movimientos = movimientos.filter(function (mov) {
    const fechaMov = new Date(mov.fecha);
    return fechaMov >= fechaLimite;
  });

  // Guarda los movimientos filtrados y reinicia la página
  movimientosFiltrados = movimientos;
  paginaActual = 1;

  // Muestra los movimientos filtrados con paginación
  mostrarMovimientosPaginados();
}

// Carga los movimientos desde localStorage o crea datos hardcodeados si no existen.
function cargarMovimientos() {
  // Obtiene movimientos desde localStorage o crear movimientos por defecto
  let movimientos = JSON.parse(localStorage.getItem("movimientos"));

  // Si no hay movimientos, crea datos hardcodeados
  if (!movimientos || movimientos.length === 0) {
    movimientos = [
      // 3 Ingresos (total: 18,500)
      {
        tipo: "deposito",
        monto: 8000,
        descripcion: "Depósito inicial",
        mensaje: "Carga de fondos a la cuenta",
        fecha: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000).toISOString(), // 15 días atrás
      },
      {
        tipo: "deposito",
        monto: 5500,
        descripcion: "Recarga de saldo",
        mensaje: "Transferencia desde cuenta bancaria",
        fecha: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString(), // 10 días atrás
      },
      {
        tipo: "recibido",
        monto: 5000,
        descripcion: "Pago recibido de Juan Pérez",
        mensaje: "Gracias por el servicio",
        fecha: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(), // 5 días atrás
      },
      // 4 Egresos (total: 6,000) - Para que el saldo final sea 12,500
      {
        tipo: "envio",
        monto: 1500,
        descripcion: "Envío a María González",
        mensaje: "Pago de servicios",
        fecha: new Date(Date.now() - 12 * 24 * 60 * 60 * 1000).toISOString(), // 12 días atrás
      },
      {
        tipo: "envio",
        monto: 2000,
        descripcion: "Envío a Carlos Pérez",
        mensaje: "Préstamo personal",
        fecha: new Date(Date.now() - 8 * 24 * 60 * 60 * 1000).toISOString(), // 8 días atrás
      },
      {
        tipo: "envio",
        monto: 1800,
        descripcion: "Envío a Ana Rodríguez",
        mensaje: "Compra compartida",
        fecha: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(), // 4 días atrás
      },
      {
        tipo: "envio",
        monto: 700,
        descripcion: "Envío a Pedro López",
        mensaje: "Pago de cena",
        fecha: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(), // 2 días atrás
      },
    ];

    // Ordena movimientos por fecha (más recientes primero)
    movimientos.sort((a, b) => new Date(b.fecha) - new Date(a.fecha));

    // Guarda los movimientos hardcodeados en localStorage
    localStorage.setItem("movimientos", JSON.stringify(movimientos));
  }

  // Calcula totales de ingresos y egresos
  let totalIngresos = 0;
  let totalEgresos = 0;

  movimientos.forEach(function (mov) {
    if (mov.tipo === "deposito" || mov.tipo === "recibido") {
      totalIngresos += mov.monto;
    } else if (mov.tipo === "envio") {
      totalEgresos += mov.monto;
    }
  });

  // Actualiza tarjetas de ingresos y egresos
  $(".card.text-center")
    .eq(0)
    .find("h4")
    .text(`$${formatearPesos(totalIngresos)}`);
  $(".card.text-center")
    .eq(1)
    .find("h4")
    .text(`$${formatearPesos(totalEgresos)}`);

  // Guarda movimientos en variable global y muestra con paginación
  movimientosFiltrados = movimientos;
  paginaActual = 1;
  mostrarMovimientosPaginados();
}

// Muestra los movimientos de la página actual con paginación.
function mostrarMovimientosPaginados() {
  const totalPaginas = Math.ceil(movimientosFiltrados.length / itemsPorPagina);
  const inicio = (paginaActual - 1) * itemsPorPagina;
  const fin = inicio + itemsPorPagina;
  const movimientosPagina = movimientosFiltrados.slice(inicio, fin);

  mostrarMovimientos(movimientosPagina);
  actualizarPaginacion(totalPaginas);
}

// Actualiza los controles de paginación según la página actual y total de páginas.
function actualizarPaginacion(totalPaginas) {
  const paginacion = $(".pagination");
  paginacion.empty();

  // Botón Anterior
  const anteriorDisabled = paginaActual === 1 ? "disabled" : "";
  paginacion.append(`
    <li class="page-item ${anteriorDisabled}">
      <a class="page-link" href="#" data-pagina="${paginaActual - 1}">
        <i class="bi bi-chevron-left"></i>
        Anterior
      </a>
    </li>
  `);

  // Páginas numeradas
  for (let i = 1; i <= totalPaginas; i++) {
    const activeClass = i === paginaActual ? "active" : "";
    paginacion.append(`
      <li class="page-item ${activeClass}">
        <a class="page-link" href="#" data-pagina="${i}">${i}</a>
      </li>
    `);
  }

  // Botón Siguiente
  const siguienteDisabled =
    paginaActual === totalPaginas || totalPaginas === 0 ? "disabled" : "";
  paginacion.append(`
    <li class="page-item ${siguienteDisabled}">
      <a class="page-link" href="#" data-pagina="${paginaActual + 1}">
        Siguiente
        <i class="bi bi-chevron-right"></i>
      </a>
    </li>
  `);
}

// Agrega eventos a los controles de paginación.
function agregarEventosPaginacion() {
  $(document).on("click", ".pagination .page-link", function (e) {
    e.preventDefault();
    const pagina = parseInt($(this).data("pagina"));
    const totalPaginas = Math.ceil(
      movimientosFiltrados.length / itemsPorPagina
    );

    if (!isNaN(pagina) && pagina >= 1 && pagina <= totalPaginas) {
      paginaActual = pagina;
      mostrarMovimientosPaginados();

      // Scroll suave al inicio de la lista
      $(".transaction-list")
        .get(0)
        ?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  });
}

// Muestra los movimientos en la lista.
function mostrarMovimientos(movimientos) {
  const listaMovimientos = $("#lista-movimientos");

  // Actualiza el badge de cantidad con el total de movimientos filtrados
  const totalMovimientos = movimientosFiltrados.length;
  if (totalMovimientos === 0) {
    $("#badge-cantidad").text("Sin movimientos");
  } else if (totalMovimientos === 1) {
    $("#badge-cantidad").text("1 movimiento");
  } else {
    $("#badge-cantidad").text(`${totalMovimientos} movimientos`);
  }

  if (movimientos.length === 0) {
    // Muestra mensaje cuando no hay movimientos
    listaMovimientos.html(`
      <div class="text-center py-5">
        <div class="mb-4">
          <i class="bi bi-inbox empty-state-icon-large"></i>
        </div>
        <h6 class="text-muted mb-2">No hay movimientos que mostrar</h6>
        <p class="text-muted small mb-0">
          <i class="bi bi-info-circle me-1"></i>
          Realiza un depósito o envío para ver tu historial
        </p>
      </div>
    `);
    return;
  }

  // Limpia la lista y crea el elemento ul
  listaMovimientos.html('<ul class="list-group list-group-flush"></ul>');
  const ul = listaMovimientos.find("ul");

  // Agrega cada movimiento
  movimientos.forEach(function (mov) {
    const elemento = crearElementoMovimiento(mov);
    ul.append(elemento);
  });
}

// Crea el elemento HTML para un movimiento.
function crearElementoMovimiento(movimiento) {
  // Determina tipo de movimiento
  let icono, colorClass, signo, titulo;

  if (movimiento.tipo === "deposito") {
    icono = "bi-arrow-down-circle-fill";
    colorClass = "success";
    signo = "+";
    titulo = "Depósito recibido";
  } else if (movimiento.tipo === "envio") {
    icono = "bi-arrow-up-circle-fill";
    colorClass = "danger";
    signo = "-";
    titulo = "Envío de dinero";
  } else if (movimiento.tipo === "recibido") {
    icono = "bi-arrow-down-circle-fill";
    colorClass = "success";
    signo = "+";
    titulo = "Dinero recibido";
  }

  // Formatea fecha
  const fecha = new Date(movimiento.fecha);
  const fechaFormateada =
    fecha.toLocaleDateString("es-CL", {
      day: "2-digit",
      month: "short",
      year: "numeric",
    }) +
    ", " +
    fecha.toLocaleTimeString("es-CL", {
      hour: "2-digit",
      minute: "2-digit",
    });

  // Crea el elemento
  const li = $("<li></li>").addClass("list-group-item py-3").html(`
      <div class="d-flex justify-content-between align-items-start">
        <div class="d-flex">
          <div class="bg-${colorClass} bg-opacity-10 text-${colorClass} rounded-circle d-flex align-items-center justify-content-center me-3 stat-circle-icon">
            <i class="bi ${icono}"></i>
          </div>
          <div>
            <h6 class="mb-1">${movimiento.descripcion || titulo}</h6>
            <small class="text-muted">
              <i class="bi bi-calendar3 me-1"></i>
              ${fechaFormateada}
            </small>
            ${
              movimiento.mensaje
                ? `<br><small class="text-muted"><i class="bi bi-chat-left-text me-1"></i>"${movimiento.mensaje}"</small>`
                : ""
            }
          </div>
        </div>
        <div class="text-end">
          <strong class="text-${colorClass}">${signo}$${formatearPesos(
    movimiento.monto
  )}</strong>
          <br>
          <span class="badge bg-success bg-opacity-10 text-success mt-1">Completado</span>
        </div>
      </div>
    `);

  return li;
}

// Obtiene el nombre legible del tipo de transacción.
function getTipoTransaccion(tipo) {
  switch (tipo) {
    case "deposito":
      return "Depósito";
    case "envio":
      return "Envío";
    case "recibido":
      return "Recibido";
    default:
      return "Movimiento";
  }
}
