module.exports = {
    publicPath: "/",
    configureWebpack: config => {
        config.externals = {
            vue: 'Vue',
            axios: 'Axios',
            vuerouter: 'Vuerouter',
            vuerouter: 'Vuerouter',
            'element-ui': 'ElementUI',
        }
    },
}