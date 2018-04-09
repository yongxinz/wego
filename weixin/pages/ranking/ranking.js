var app = getApp();

Page({
    data: {
        tabs: ['个人数据', '全国排名'],
        is_ready: false,
        activeIndex: 0,
        sliderOffset: 0,
        winWidth: 0,
        winHeight: 0,
        ranks: [],
        personal: {},
        gData: null,
        results: {}
    },

    onLoad: function () {
        var that = this;

        wx.getSystemInfo({
            success: function (res) {
                that.setData({
                    winWidth: res.windowWidth,
                    winHeight: res.windowHeight
                });
            }
        });

        app.helper.wxPromisify(wx.getUserInfo)().then(function (res) {
            app.config.gData.userInfo = res.userInfo;
            that.setData({'gData.userInfo': app.config.gData.userInfo, is_ready: true});
            app.helper.waitUserSid(that.getApiUserData);
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
        app.helper.waitUserSid(this.getPersonalData);
    },

    getApiData: function () {
        let that = this;
        app.helper.getApi('werun').then(function (res) {
            that.setData({ranks: res.data.results})
        });
    },

    getPersonalData: function () {
        let that = this;
        app.helper.getApi('personal').then(function (res) {
            that.setData({personal: res.data.results})
        });
    },

    bindChange: function (e) {
        var that = this;
        that.setData({currentTab: e.detail.current});
    },

    tabClick: function (e) {
        this.setData({
            sliderOffset: e.currentTarget.offsetLeft,
            activeIndex: e.currentTarget.id
        });

        if (this.data.activeIndex === 0) {
            app.helper.waitUserSid(this.getPersonalData);
        } else {
            app.helper.waitUserSid(this.getApiData);
        }
    },

    sharePic: function (e) {
        let item = e.currentTarget.dataset.item;
        let type = e.currentTarget.dataset.type;
        let gather = e.currentTarget.dataset.gather;
        wx.navigateTo({ url: './share/share?item=' + item + '&type=' + type + '&gather=' + gather })
    },

    updateUsers: function () {
        let that = this;

        app.helper.putApi('users', that.data.gData, this.data.results.id + '/nickname/').then(function (res) {
            console.log(res)
        })
    },

    getApiUserData: function () {
        let that = this;

        app.helper.getApi('users').then(function (res) {
            that.setData({results: res.data.results[0]});
        }).then(function (res) {
            app.helper.waitUserSid(that.updateUsers);
        });
    }
});
