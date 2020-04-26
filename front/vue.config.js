const CompressionPlugin = require('compression-webpack-plugin');

module.exports = {
  runtimeCompiler: true,
  productionSourceMap: false,
  publicPath: process.env.BASE_URL || '/admin/',

  css: {
    extract: true
  },

  configureWebpack: {
    // No need for splitting
    optimization: {
      splitChunks: {
        chunks: 'all'
      }
    }
  },

  chainWebpack(config) {
    config.plugins.delete('prefetch');

    // and this line
    config.plugin('CompressionPlugin').use(CompressionPlugin);
  },

  pluginOptions: {
    i18n: {
      locale: 'en',
      fallbackLocale: 'en',
      localeDir: 'locales',
      enableInSFC: true
    }
  }
}
