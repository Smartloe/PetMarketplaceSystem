const path = require('path')
module.exports = {
    publicPath: '/',
    outputDir: 'dist',
    assetsDir: 'static',
    productionSourceMap: false,
    devServer: {
        hot: true,
        port: 8010,
        open: true,
        proxy: {
            '/': {
                target: 'http://127.0.0.1:8000/',
                changeOrigin: true,
                pathRewrite: {'^/': ''},
            },
        },
    },
    configureWebpack: {
        name: 'system',
        resolve: {
            alias: {
                "~@": __dirname,
                "@": path.resolve(__dirname, "./src")
            }
        }
    },
}
