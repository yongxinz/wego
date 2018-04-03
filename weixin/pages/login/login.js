const app = getApp();

Page({
    data: {
        mobile: '',
        msg: '',
        countDown: false,
        countDownSecond: 60,
        countDownCron: '',
        showInput: false
    },
    bindSubmit: function (e) {
        let that = this;
        // 验证手机验证码
        app.helper.postApi('join', e.detail.value).then(function (res) {
            if (res.data.status) {
                app.config.gData.mobile = res.data.user.mobile;
                clearInterval(that.data.countDownCron);
                wx.reLaunch({url: '/pages/index/index'});
            } else {
                that.setData({msg: res.data.msg});
            }
        });
    },
    bindGetSms: function () {
        if (!this.data.countDown) {
            let that = this;
            // 发送手机验证码
            app.helper.postApi('join', {
                mobile: that.data.mobile
            }).then(function (res) {
                that.setData({msg: res.data.msg});
                if (res.data.status) {
                    that.setData({countDown: true});
                    that.setData({
                        countDownCron: setInterval(function () {
                            let tmp = that.data.countDownSecond;
                            that.setData({
                                countDownSecond: tmp - 1
                            });

                            if (that.data.countDownSecond === 0) {
                                that.setData({
                                    countDown: false,
                                    countDownSecond: 60
                                });
                                clearInterval(that.data.countDownCron);
                            }
                        }, 1000)
                    })
                }
            });
        }
    },
    bindKeyInput: function (e) {
        this.setData({
            mobile: e.detail.value
        });
    },
    getPhoneNumber: function (e) {
        let that = this;
        if (e.detail.errMsg === 'getPhoneNumber:ok') {
            // 获取手机号
            app.helper.postApi('join2wx', e.detail).then(function (res) {
                if (res.data.status) {
                    app.config.gData.mobile = res.data.mobile;
                    wx.reLaunch({url: '/pages/index/index'});
                } else {
                    that.setData({msg: res.data.msg});
                }
            });
        }
    },

    showInput: function () {
        this.setData({showInput: true})
    }
});