module.exports = {
  // Build assets for Django to serve from /static/dist/
  publicPath: '/static/dist/',
  outputDir: '../static/dist',
  filenameHashing: false,
  transpileDependencies: [],

  // Dev server settings (optional, for local dev)
  configureWebpack: {
    devServer: {
      devMiddleware: { writeToDisk: true }
    }
  },

  // Do not emit index.html; Django provides the HTML templates.
  chainWebpack: (config) => {
    if (config.plugins.has('html')) config.plugins.delete('html')
    if (config.plugins.has('preload')) config.plugins.delete('preload')
    if (config.plugins.has('prefetch')) config.plugins.delete('prefetch')
    if (config.plugins.has('copy')) {
      config.plugin('copy').tap((args) => {
        const first = args[0] || {};
        const patterns = first.patterns || [];
        patterns.forEach((p) => {
          if (!p.globOptions) p.globOptions = {};
          if (!p.globOptions.ignore) p.globOptions.ignore = [];
          if (!p.globOptions.ignore.includes('index.html')) {
            p.globOptions.ignore.push('index.html');
          }
        });
        return args;
      });
    }
  },
};
