// 1. Instrucción para crear y cargar la librería de Google desde su servidor
var script1 = document.createElement('script');
script1.async = true;
script1.src = 'https://googletagmanager.com';
document.head.appendChild(script1);

// 2. Instrucción para activar el rastreador con tu ID de la web
var script2 = document.createElement('script');
script2.innerHTML = `
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-9RKWSS4K6B');
`;
document.head.appendChild(script2);
