let EventEmitter = require('./event-emitter');

let baseURL = 'https://wego.lvzhouhuwai.com/api';
// baseURL = 'http://192.168.8.110:8810/api';

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
    info: '/passport/wx/info/',
    home: '/passport/wx/check/',
    share_info: '/passport/wx/share_info/',
    get_applet_image: '/passport/wx/applet_image/',
    cancel: '/passport/wx/cancel/',
    join2wx: '/passport/wx/join2wx/',
    werun: '/werun/',
    today: '/werun/today/',
    ranking: '/werun/ranking/',
    personal: '/werun/personal/',
    users: '/users/',
    summary: '/define/summary/',
    summary_pic: '/summary_pic/get_summary_pic/',
    activity_define: '/activity/define/all/',
    activity_join: '/activity/list/',
    activity_detail: '/activity/list/detail/',
    activity_summary: '/activity/list/summary/',
    payments: '/activity/list/payments/',
    is_join: '/activity/list/is_join/',
    get_title_pic: '/get_title_pic/',
    fabulous: '/fabulous/',
    content: '/activity/define/content/'
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