var app = getApp();

Page({
    data: {
        windowWidth: 0,
        windowHeight: 0,
        radius: 110,
        encryptedData: '',
        iv: '',
        results: {},
        targetFlag: 0
    },

    onLoad: function (options) {
        let that = this;
        wx.getSystemInfo({
            success: function (res) {
                that.setData({
                    windowWidth: res.windowWidth,
                    windowHeight: res.windowHeight,
                    radius: res.windowWidth / 2 - 142 / 2
                });
            }
        });

        // 检验小程序是否绑定手机号
        app.helper.waitUserSid(function () {
            app.helper.checkJoin().then(function (res) {
                app.config.gData.mobile = res.data.user.mobile;
                that.setData({'gData.mobile': app.config.gData.mobile})
            });
        });
    },

    onShow: function () {
        let that = this;

        var cxt_arc = wx.createCanvasContext('canvasCircle');
        that.drawCircle(cxt_arc, '#eeeeee', 3.5 * Math.PI);

        // 获取微信运动权限
        app.helper.wxPromisify(wx.getWeRunData)().then(function (res) {
            that.setData({'encryptedData': res.encryptedData, 'iv': res.iv});
            app.helper.waitUserSid(that.submitWeRunData)
        }).catch(function (res) {
            wx.showModal({
                title: '微信授权',
                content: '为获得最佳体验，请按确定并在授权管理中选中“微信运动步数”，再重新进入小程序即可正常使用。',
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

    submitWeRunData: function () {
        let that = this;
        app.helper.postApi('werun', {'encryptedData': this.data.encryptedData, 'iv': this.data.iv}).then(function (res) {
            app.helper.waitUserSid(that.getApiData)
        });
    },

    getApiData: function () {
        let that = this;

        app.helper.getApi('today').then(function (res) {
            let targetFlag = res.data.results.step/res.data.results.target;
            that.setData({results: res.data.results, targetFlag: targetFlag});

            var cxt_arc = wx.createCanvasContext('canvasArcCir');
            that.drawCircle(cxt_arc, '#d81e06', (2 * targetFlag + 1.5) * Math.PI)
        })
    },

    drawCircle: function (cxt_arc, color, endAngle) {
        cxt_arc.setLineWidth(25);
        cxt_arc.setStrokeStyle(color);
        cxt_arc.setLineCap('round');
        cxt_arc.beginPath();
        cxt_arc.arc(this.data.windowWidth / 2, this.data.windowWidth / 2 - 71 + 57.5, this.data.radius, 1.5 * Math.PI, endAngle, false);
        cxt_arc.stroke();
        cxt_arc.draw();
    }
});
