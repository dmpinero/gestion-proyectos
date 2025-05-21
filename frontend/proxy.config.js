const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:8000',
      changeOrigin: true,
      secure: false,
      pathRewrite: {
        '^/api': '',
      },
      onProxyReq: (proxyReq, req, res) => {
        // Opcional: Agregar encabezados personalizados si es necesario
        proxyReq.setHeader('X-Forwarded-Host', 'localhost:3000');
      },
      onError: (err, req, res) => {
        console.error('Error en el proxy:', err);
        res.status(500).json({ error: 'Error en el servidor proxy' });
      },
    })
  );
};
