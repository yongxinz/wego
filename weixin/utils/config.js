let EventEmitter = require('./event-emitter');

// let baseURL = 'https://shop.youmutou.com/api/v1';
let baseURL = 'http://192.168.8.110:8810/api';

try {
    let res = wx.getSystemInfoSync();
    if (res.platform === 'devtools') {
        // baseURL = 'http://127.0.0.1:8810/api';
        baseURL = 'http://192.168.8.110:8810/api';
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
    cancel: '/passport/wx/cancel/',
    join2wx: '/passport/wx/join2wx/',
    werun: '/werun/',
    today: '/werun/today/',
    personal: '/werun/personal/',
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