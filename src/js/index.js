// Función principal se ejecuta cuando el DOM está completamente cargado.
$(document).ready(function () {
  // Botón de ingreso
  $(".btn-primary").on("click", function (e) {
    e.preventDefault();
    const $btn = $(this);
    const href = $btn.attr("href");

    // Redirige después de la animación
    setTimeout(function () {
      window.location.href = href;
    }, 500);
  });

  // Animación de los iconos al hacer hover
  $(".feature-icon").hover(
    function () {
      $(this).find("i").addClass("animate__animated animate__bounceIn");
    },
    function () {
      $(this).find("i").removeClass("animate__animated animate__bounceIn");
    }
  );
});
