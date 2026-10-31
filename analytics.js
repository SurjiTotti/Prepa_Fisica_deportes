// 1. Creamos el elemento para la librería de Google
var gaScript = document.createElement('script');
gaScript.async = true;
gaScript.src = 'https://googletagmanager.com';

// 2. TRUCO: Esperamos a que la librería se cargue por completo antes de activarla
gaScript.onload = function() {
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-9RKWSS4K6B');
};

// 3. Insertamos el script en la web
document.head.appendChild(gaScript);
