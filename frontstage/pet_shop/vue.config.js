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
            '/api': {
                target: 'http://127.0.0.1:8000/',
                changeOrigin: true,
                pathRewrite: {'^/api': ''},
            },
        },
    },
    configureWebpack: {
        name: 'system',
        resolve: {
            alias: {
                "~@": __dirname,
                "@": path.resolve(__dirname, "src")
            }
        },
        module: {
            rules: [
                {
                    test: /\.mjs$/,
                    include: /node_modules/,
                    type: 'javascript/auto'
                },

            ]
        }
    },
}

