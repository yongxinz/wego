var app = getApp();

var varName;
var ctx = wx.createCanvasContext('canvasArcCir');

Page({
    data: {
        windowWidth: 0,
        windowHeight: 0,
        encryptedData: '',
        iv: '',
        step: 0
    },

    onLoad: function (options) {
        let that = this;
        wx.getSystemInfo({
            success: function (res) {
                that.setData({
                    windowWidth: res.windowWidth,
                    windowHeight: res.windowHeight
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
        //创建并返回绘图上下文context对象。
        var cxt_arc = wx.createCanvasContext('canvasCircle');
        cxt_arc.setLineWidth(25);
        cxt_arc.setStrokeStyle('#eaeaea');
        cxt_arc.setLineCap('round');
        cxt_arc.beginPath();
        cxt_arc.arc(this.data.windowWidth / 2, this.data.windowWidth / 2, 110, 0, 2 * Math.PI, false);
        cxt_arc.stroke();
        cxt_arc.draw();

        // 获取微信运动权限
        let that = this;
        app.helper.wxPromisify(wx.getWeRunData)().then(function (res) {
            that.setData({'encryptedData': res.encryptedData, 'iv': res.iv});
            that.submitWeRunData();
        }).then(
            app.helper.waitUserSid(that.getApiData)
        ).catch(function (res) {
            wx.showModal({
                title: '用户未授权',
                content: '如需正常使用计步功能，请按确定并在授权管理中选中“微信运动”，然后点按确定。最后再重新进入小程序即可正常使用。',
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
        app.helper.postApi('werun', {'encryptedData': this.data.encryptedData, 'iv': this.data.iv}).then(function (res) {
            console.log(res);
        });
    },

    getApiData: function () {
        let that = this;

        app.helper.getApi('today').then(function (res) {
            that.setData({step: res.data.results.step});
        })
    },

    drawCircle: function () {
        let that = this;
        clearInterval(varName);
        function drawArc(s, e) {
            ctx.setFillStyle('white');
            ctx.clearRect(0, 0, 250, 250);
            ctx.draw();
            var x = 150, y = 150, radius = 110;
            ctx.setLineWidth(25);
            ctx.setStrokeStyle('#d81e06');
            ctx.setLineCap('round');
            ctx.beginPath();
            ctx.arc(that.data.windowWidth / 2, that.data.windowWidth / 2, radius, s, e, false);
            ctx.stroke();
            ctx.draw()
        }

        var step = 1, startAngle = 1.5 * Math.PI, endAngle = 0;
        var animation_interval = 1000, n = 60;
        var animation = function () {
            if (step <= n) {
                endAngle = step * 2 * Math.PI / n + 1.5 * Math.PI;
                drawArc(startAngle, endAngle);
                step++;
            } else {
                clearInterval(varName);
            }
        };
        varName = setInterval(animation, animation_interval);
    }
});
