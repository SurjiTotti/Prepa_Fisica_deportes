(function () {
  var GA_ID = 'G-9RKWSS4K6B';
  var KEY = 'cookies_analytics';
  // Ruta base de la web, calculada a partir de donde está este archivo
  var base = document.currentScript.src.replace(/analytics\.js.*$/, '');

  function leer() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function guardar(v) {
    try { localStorage.setItem(KEY, v); } catch (e) {}
  }

  function cargarAnalytics() {
    if (window.gaCargado) return;
    window.gaCargado = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag('js', new Date());
    gtag('config', GA_ID);
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  }

  function mostrarBanner() {
    if (document.getElementById('cookie-banner')) return;

    var css = document.createElement('style');
    css.textContent =
      '#cookie-banner{position:fixed;left:0;right:0;bottom:0;z-index:100;background:#111;color:#fff;' +
      'padding:16px 20px;display:flex;flex-wrap:wrap;align-items:center;gap:12px 20px;' +
      'border-top:4px solid #e4002b;font:15px/1.5 system-ui,Arial,sans-serif}' +
      '#cookie-banner p{margin:0;flex:1 1 320px}' +
      '#cookie-banner a{color:#fff}' +
      '#cookie-banner .acciones{display:flex;gap:10px}' +
      '#cookie-banner button{cursor:pointer;padding:10px 20px;border:2px solid #e4002b;' +
      'background:#e4002b;color:#fff;font:800 .8rem system-ui,Arial,sans-serif;' +
      'letter-spacing:.08em;text-transform:uppercase}' +
      '#cookie-banner button.rechazar{background:transparent;border-color:#fff}';
    document.head.appendChild(css);

    var b = document.createElement('div');
    b.id = 'cookie-banner';
    b.setAttribute('role', 'dialog');
    b.setAttribute('aria-label', 'Aviso de cookies');
    b.innerHTML =
      '<p>Usamos cookies de analítica (Google Analytics) para saber qué guías se leen más. ' +
      'Solo se activan si las aceptas. <a href="' + base + 'privacidad.html">Más información</a></p>' +
      '<div class="acciones">' +
      '<button type="button" class="rechazar">Rechazar</button>' +
      '<button type="button" class="aceptar">Aceptar</button></div>';
    document.body.appendChild(b);

    b.querySelector('.aceptar').onclick = function () {
      guardar('si');
      b.remove();
      cargarAnalytics();
    };
    b.querySelector('.rechazar').onclick = function () {
      guardar('no');
      b.remove();
    };
  }

  function iniciar() {
    var estado = leer();
    if (estado === 'si') cargarAnalytics();
    else if (estado !== 'no') mostrarBanner();

    // Cualquier enlace con data-cookies vuelve a abrir el banner
    document.addEventListener('click', function (e) {
      var el = e.target.closest && e.target.closest('[data-cookies]');
      if (el) {
        e.preventDefault();
        try { localStorage.removeItem(KEY); } catch (err) {}
        mostrarBanner();
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciar);
  } else {
    iniciar();
  }
})();
