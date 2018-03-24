const app = getApp();

Page({
    data: {
        gData: null,
        is_ready: false,
        results: {}
    },

    onLoad: function () {
        let that = this;

        // app.helper.waitUserSid(function () {
        //     app.helper.checkJoin().then(function (res) {
        //         app.config.gData.mobile = res.data.user.mobile;
        //         that.setData({'gData.mobile': app.config.gData.mobile})
        //     });
        // });
    },

    onShow: function () {
        let that = this;

        app.helper.wxPromisify(wx.getUserInfo)().then(function (res) {
            app.config.gData.userInfo = res.userInfo;
            that.setData({'gData.userInfo': app.config.gData.userInfo, is_ready: true});
            that.setData({gData: app.config.gData});

            app.helper.waitUserSid(that.getApiData);
        }).catch(function (res) {
            wx.showModal({
                title: '微信授权',
                content: '为获得最佳体验，请按确定并在授权管理中选中“用户信息”，再重新进入小程序即可正常使用。',
                showCancel: false,
                success: function (res) {
                    if (res.confirm) {
                        wx.openSetting({
                            success: function success(res) {
                                console.log('openSetting success', res.authSetting);
                            }
                        });
                    }
                }
            })
        });
    },

    updateUsers: function () {
        let that = this;

        app.helper.putApi('users', that.data.gData, this.data.results.id + '/nickname/').then(function (res) {
            console.log(res)
        })
    },

    getApiData: function () {
        let that = this;

        app.helper.getApi('users').then(function (res) {
            that.setData({results: res.data.results[0]});
        }).then(function (res) {
            app.helper.waitUserSid(that.updateUsers);
        })
    },

    // 获取用户头像昵称
    bindGetUserinfo: function (res) {
        app.config.gData.userInfo = res.detail.userInfo;
        this.setData({'gData.userInfo': res.detail.userInfo});

        app.helper.waitUserSid(this.updateUsers);
    },

    updateTarget(e) {
        wx.navigateTo({url: e.currentTarget.dataset.url})
    },

    mobBind: function () {
        wx.navigateTo({url: '/pages/login/login'})
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
