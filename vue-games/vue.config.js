// const { defineConfig } = require('@vue/cli-service')
// module.exports = defineConfig({
//   transpileDependencies: true
// })
module.exports = {
  // In production we serve built files from Django static
  publicPath: '/static/dist/',
  outputDir: '../static/dist',
  filenameHashing: false, // ensure stable filenames: app.js, chunk-vendors.js, css files

  // Keep dev server behavior for local development if used
  configureWebpack: {
    devServer: {
      devMiddleware: { writeToDisk: true }
    }
  }
};
