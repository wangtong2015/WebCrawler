// vue.config.js
module.exports = {
    assetsDir: 'static',
    devServer: {
        proxy: {
            '/spider': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true
                // pathRewrite: {'^/api': ''}
            }
        }
    }
};