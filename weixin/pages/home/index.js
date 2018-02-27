const app = getApp();

Page({
    data: {
        gData: null,
        is_ready: false
    },

    onLoad: function () {
        let that = this;

        // app.helper.waitUserSid(function () {
        //     app.helper.checkJoin().then(function (res) {
        //         app.config.gData.mobile = res.data.user.mobile;
        //         that.setData({'gData.mobile': app.config.gData.mobile})
        //     });
        // });

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

    onShow: function () {
        this.setData({gData: app.config.gData});
        app.helper.waitUserSid(this.updateUsers);
    },

    updateUsers: function () {
        let that = this;

        app.helper.postApi('nickname', that.data.gData).then(function (res) {
            console.log(res)
        })
    },

    // 获取用户头像昵称
    bindGetUserinfo: function (res) {
        app.config.gData.userInfo = res.detail.userInfo;
        this.setData({'gData.userInfo': res.detail.userInfo});

        app.helper.waitUserSid(this.updateUsers);
    },

    mobBind: function () {
        wx.navigateTo({url: '/pages/login/index'})
    },

    cancelBind: function () {
        let that = this;
        app.helper.getApi('cancel').then(function (res) {
            if (res.data.status) {
                app.config.gData.mobile = '';
                that.setData({'gData.mobile': app.config.gData.mobile})
            }
        })
    }
});
