let EventEmitter = require('./event-emitter');

// let baseURL = 'https://shop.youmutou.com/api/v1';
let baseURL = 'http://192.168.8.100:8810/api';

try {
    let res = wx.getSystemInfoSync();
    if (res.platform === 'devtools') {
        baseURL = 'http://127.0.0.1:8810/api';
    }
} catch (e) {
    // Do something when catch error
}

module.exports.baseURL = baseURL;

module.exports.apiMap = {
    login: '/passport/wx/login/',
    join: '/passport/wx/join/',
    check: '/passport/wx/check/',
    home: '/passport/wx/check/',
    share_info: '/passport/wx/share_info/',
    get_applet_image: '/passport/wx/applet_image/',
    categorys: '/support/categorys/',
    supply: '/supplier/supply/',
    supply_attention: '/supplier/supply_attention/',
    supply_all_attention: '/supplier/supply_all_attention/',
    futures: '/supplier/futures/',
    futures_inquiry: '/supplier/futures_inquiry/',
    cart: '/shop/cart/',
    cart_all_nums: '/shop/cart/all_nums/',
    cart_items: '/shop/cart_items/',
    get_product_list: '/get_product_list/',
    order: '/shop/order/',
    orderpay: '/shop/order_pay/',
    address: '/shop/order_user/',
    get_order_user: '/shop/get_order_user/',
    mall: '/mall_wms/',
    mall_more: '/mall_wms_more/',
    company: '/company/',
    cancel: '/passport/wx/cancel/',
    join2wx: '/passport/wx/join2wx/',
    trust: '/support/trust/',
    trust_quotes: '/support/trust_quotes/',
    dealer: '/dealer/',
    get_source_city: '/get_source_city/',
    werun: '/data/werun/',
    nickname: '/users/nickname/'
};


module.exports.emitter = new EventEmitter();


module.exports.gData = {
    code: '',
    userSid: null,
    mobile: '',
    userInfo: null,
    extraData: {},
    scene: ''
};