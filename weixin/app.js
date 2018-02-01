const helper = require('./utils/helper_business');
const config = require('./utils/config');

App({
    helper: helper,
    config: config,

    onLaunch: function () {
        let that = this;
        // 获取用户基础信息, 微信已知bug，app中getSetting不执行，暂时放到页面内获取
        // helper.wxPromisify(wx.getSetting)().then(function (res) {
        //     if (res.authSetting['scope.userInfo']) {
        //         // 获取用户微信基础信息
        //         helper.wxPromisify(wx.getUserInfo)().then(function (res) {
        //             config.gData.userInfo = res.userInfo;
        //             config.emitter.emit('userInfo');
        //         });
        //     }
        // });

        // 微信登录，获取用户code
        helper.wxPromisify(wx.login)().then(function (res) {
            // 登录后端, wx code -> dj sid
            helper.wxPromisify(wx.request)({
                url: config.baseURL + '/passport/wx/login/',
                data: {code: res.code},
            }).then(function (res) {
                config.gData.userSid = res.data.sid;
                config.emitter.emit('userSid');
            }).catch(function (res) {
                console.error(res.errMsg)
            });
        }).catch(function (res) {
            console.error(res.errMsg)
        });
    },

    onShow: function (options) {
        config.gData.scene = options.scene;
        if (config.gData.scene === 1037) {
            config.gData.extraData = options.referrerInfo.extraData;
        }
    }
});