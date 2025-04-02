const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,

  // Run on a safe custom port so it's not blocked by PostgreSQL or Django
  devServer: {
    port: 3000, // use 3000 instead of 8080 to avoid conflict
    open: true, // automatically open the browser
    proxy: {
      // Proxy API requests to Django backend (to avoid CORS issues)
      '^/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  },

  // For production build compatibility (if you later host on Django)
  publicPath: '/',
  outputDir: 'dist',
  assetsDir: '',
  productionSourceMap: false
})
