const app = getApp();

Page({
    data: {
        gData: null,
        is_ready: false,
        results: {}
    },

    onLoad: function () {
        let that = this;

        app.helper.wxPromisify(wx.getUserInfo)().then(function (res) {
            app.config.gData.userInfo = res.userInfo;
            that.setData({'gData.userInfo': app.config.gData.userInfo, is_ready: true});
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

    onShow: function () {
        app.helper.waitUserSid(this.getApiData);
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
        });

        app.helper.getApi('info').then(function (res) {
            that.setData({'gData.mobile': res.data.user.username});
        })
    },

    updateTarget(e) {
        wx.navigateTo({url: e.currentTarget.dataset.url})
    },

    cancelBind: function () {
        let that = this;
        app.helper.getApi('cancel').then(function (res) {
            if (res.data.status) {
                app.config.gData.mobile = '';
                that.setData({'gData.mobile': app.config.gData.mobile});
                wx.redirectTo({url: '/pages/login/login'})
            }
        })
    }
});
