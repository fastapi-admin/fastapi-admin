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
  
}