export default [
    // 首页
    {
        path: '/',
        name: '000',
        label: '首页',
        component: resolve => require(['./pages/welcome'], resolve)
    },
    {
        path: '/login',
        name: '000-1',
        label: '登录',
        meta: {auth: false},
        component: resolve => require(['./pages/login'], resolve)
    },
    {
        path: '/join',
        name: '000-2',
        label: '注册',
        meta: {auth: false},
        component: resolve => require(['./pages/join'], resolve)
    },
    {
        path: '/info',
        name: '000-3',
        label: '信息',
        meta: {auth: false},
        component: resolve => require(['./pages/info'], resolve)
    },
    // 其他
    {
        path: '*', // 其他页面，强制跳转到登录页面
        name: '999',
        redirect: '/'
    }
]
