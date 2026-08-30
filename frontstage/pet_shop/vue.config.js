const path = require('path')
const Components = require('unplugin-vue-components/webpack').default
const { ElementPlusResolver } = require('unplugin-vue-components/resolvers')

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
                target: 'http://127.0.0.1:8000',
                changeOrigin: true,
            },
        },
    },
    configureWebpack: {
        name: 'system',
        plugins: [
            // Element Plus 按需引入：模板里的 el-* 组件（含各自样式）由
            // 此插件按用到的组件自动注册；JS API 组件（ElMessage /
            // ElMessageBox）不走模板，其样式在 main.js 手动引入。
            Components({ resolvers: [ElementPlusResolver()] }),
        ],
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
