/**
 * Alke Wallet — main.js
 * Inicialización de componentes Bootstrap y comportamientos globales.
 */

document.addEventListener("DOMContentLoaded", function () {
  // Inicializar todos los tooltips de Bootstrap
  const tooltipTriggerList = document.querySelectorAll(
    '[data-bs-toggle="tooltip"]',
  );
  tooltipTriggerList.forEach(function (el) {
    new bootstrap.Tooltip(el, { trigger: "hover" });
  });

  // Inicializar todos los toasts de Bootstrap
  const toastElList = document.querySelectorAll(".toast");
  toastElList.forEach(function (el) {
    const toast = new bootstrap.Toast(el, { autohide: true, delay: 4000 });
    toast.show();
  });

  // Auto-cerrar alertas de Django messages después de 5 segundos
  const alerts = document.querySelectorAll(".alert:not(.alert-permanent)");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) {
        bsAlert.close();
      }
    }, 5000);
  });
});
