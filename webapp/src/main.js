import Vue from 'vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import axios from 'axios'
// import moment from 'moment'

import App from './App'
import routes from './routes'
import store from './store'
import components from './components/'  // 加载公共组件

import helper from './utils/helper'

Vue.use(VueRouter);
Vue.use(ElementUI);
Vue.prototype.ym_api = '/api';

axios.defaults.headers.common['Authorization'] = window.localStorage.getItem('userhashid');
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
axios.interceptors.response.use(function (response) {
    helper.checkStatus(response);
    return response;
}, function (error) {
    helper.checkStatus(error.response);
    return Promise.reject(error);
});
Vue.prototype.$http = axios;

Object.keys(components).forEach((key) => {
    let name = key.replace(/(\w)/, (v) => v.toUpperCase()); // 首字母大写
    Vue.component(`ym${name}`, components[key])
});

const router = new VueRouter({
    mode: 'history',
    base: __dirname,
    routes: routes
});

Vue.filter('moment', function (value) {
    var s = new Date(value)
    var options = { year: 'numeric', month: '2-digit', day: '2-digit' };
    var sDate = s.toLocaleDateString('zh-CN', options).replace(/\//g, '-')
    return sDate + ' ' + s.toTimeString().slice(0, 9)
});

Vue.filter('date', function (value) {
    var s = new Date(value)
    var options = { year: 'numeric', month: '2-digit', day: '2-digit' };
    var sDate = s.toLocaleDateString('zh-CN', options).replace(/\//g, '-')
    return sDate
});

router.beforeEach((to, from, next) => {
    let {auth = true} = to.meta;
    let isLogin = Boolean(window.localStorage.getItem('userhashid'));

    // if (auth && !isLogin) {
    //     return next({path: '/login'})
    // }

    Vue.prototype.ym_path = {to: to, from: from};
    store.commit('addTab', to.name);
    next()
});

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app');
