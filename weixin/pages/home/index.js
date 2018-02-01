const app = getApp();

Page({
    data: {
        gData: null,
        is_ready: false
    },
    onLoad() {
        let that = this;

        app.helper.waitUserSid(function () {
            app.helper.checkJoin().then(function (res) {
                app.config.gData.mobile = res.data.user.mobile;
                that.setData({'gData.mobile': app.config.gData.mobile})
            });
        });

        //检查配置项
        app.helper.wxPromisify(wx.getSetting)().then(function (res) {
            if (res.authSetting['scope.userInfo']) {
                // 获取用户微信基础信息
                app.helper.wxPromisify(wx.getUserInfo)().then(function (res) {
                    app.config.gData.userInfo = res.userInfo;
                    that.setData({'gData.userInfo': app.config.gData.userInfo, is_ready: true})
                })
            } else {
                that.setData({is_ready: true})
            }
        });
    },
    onShow() {
        this.setData({gData: app.config.gData});
    },
    // 获取用户头像昵称
    bindGetUserinfo: function (res) {
        app.config.gData.userInfo = res.detail.userInfo;
        this.setData({'gData.userInfo': res.detail.userInfo})
    },
    mobBind() {
        wx.navigateTo({url: '/pages/login/index'})
    },
    cancelBind() {
        let that = this;
        app.helper.getApi('cancel').then(function (res) {
            if (res.data.status) {
                app.config.gData.mobile = '';
                that.setData({'gData.mobile': app.config.gData.mobile})
            }
        })
    },
    goItem(e) {
        wx.navigateTo({url: this.data.gData.mobile ? e.currentTarget.dataset.url : '/pages/login/index'})
    }
});
