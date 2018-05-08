import util from '../../utils/util'

var app = getApp();

Page({
    data: {
        windowWidth: 0,
        windowHeight: 0,
        radius: 110,
        encryptedData: '',
        iv: '',
        results: {},
        targetFlag: 0,
        current: 0
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

        app.helper.waitUserSid(that.getActivity);
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
            var step = res.data.results.step;
            var targetFlag = step / res.data.results.target;
            that.setData({results: res.data.results, targetFlag: targetFlag});

            app.helper.getApi('activity_join_personal').then(function (res) {
                that.setData({apiDataJoin: res.data.results});
                if (res.data.results.target !== '') {
                    targetFlag = step / res.data.results.target;
                }
                var cxt_arc = wx.createCanvasContext('canvasArcCir');
                that.drawCircle(cxt_arc, '#d81e06', (2 * targetFlag + 1.5) * Math.PI)
            })
        })
    },

    getActivity: function () {
        let that = this;

        app.helper.getApi('activity_define').then(function (res) {
            that.setData({apiData: res.data.results});
        })
    },

    // getActivityJoin: function () {
    //     let that = this;
    //
    //     app.helper.getApi('activity_join').then(function (res) {
    //         that.setData({apiDataJoin: res.data.results});
    //     })
    // },

    bindChange: function (e) {
        var that = this;
        var current = e.detail.current;
        if (current > 0) {
            app.helper.getApi('activity_detail', {'activity': that.data.apiData[current-1].id}).then(function (res) {
                console.log(res)
            });
        }
    },

    bindJoinConfirm: function (e) {
        var content = '';
        var id = e.target.dataset.item.id;
        var user = e.target.dataset.item.user;
        var reward = e.target.dataset.item.reward;
        var type = e.target.dataset.item.type;

        if (type === 'D') {
            var d1 = new Date();
            var d2 = new Date(d1);
            var d3 = new Date(d1);
            d2.setDate(d1.getDate()+1);
            d3.setDate(d1.getDate()+2);
            var date_start = util.formatTime(d2);
            var date_reward = util.formatTime(d3);

            var start_time = util.formatFullTime(d2) + ' 00:00:00';
            var end_time = util.formatFullTime(d2) + ' 24:00:00';

            content = '活动时间：' + date_start + ' 00:00~24:00。挑战需要支付 ' + reward + ' 元钱，挑战成功后，奖金会在 '
                + date_reward + ' 上午 10:00 发放到微信零钱。记得在 10:00 点之前同步步数哦。'
        } else if (type === 'W') {
            var d1 = new Date();
            var d2 = new Date(d1);
            var d3 = new Date(d1);
            var d4 = new Date(d1);
            d2.setDate(d1.getDate()+1);
            d3.setDate(d1.getDate()+7);
            d4.setDate(d1.getDate()+8);
            var date_start = util.formatTime(d2);
            var date_end = util.formatTime(d3);
            var date_reward = util.formatTime(d4);

            var start_time = util.formatFullTime(d2) + ' 00:00:00';
            var end_time = util.formatFullTime(d3) + ' 24:00:00';

            content = '活动时间：' + date_start + ' 00:00~' + date_end + ' 24:00' + '挑战需要支付 ' + reward + ' 元钱，挑战成功后，奖金会在 '
                + date_reward + ' 上午 10:00 发放到微信零钱。记得在 10:00 点之前同步步数哦。'
        }

        var form = {'user': user, 'activity': id, 'start_time': new Date(start_time), 'end_time': new Date(end_time)};

        app.helper.getApi('activity_join', {'user': user, 'start_time': new Date(start_time).toISOString(),
                                            'end_time': new Date(end_time).toISOString()}).then(function (res) {
            if (res.data.results.length > 0) {
                wx.showToast({title: '参加失败，已有活动正在进行中...', icon: 'none', duration: 2000})
            } else {
                wx.showModal({
                    title: '活动信息',
                    content: content,
                    confirmText: "确定",
                    cancelText: "取消",
                    success: function (res) {
                        if (res.confirm) {
                            app.helper.postApi('activity_join', form).then(function (res) {
                                wx.showToast({title: '参加成功', icon: 'success', duration: 1000})
                            })
                        }
                    }
                });
            }
        });
    },

    drawCircle: function (cxt_arc, color, endAngle) {
        cxt_arc.setLineWidth(25);
        cxt_arc.setStrokeStyle(color);
        cxt_arc.setLineCap('round');
        cxt_arc.beginPath();
        cxt_arc.arc((this.data.windowWidth - 20) / 2, (this.data.windowWidth - 20) / 2 - 71 + 57.5, this.data.radius, 1.5 * Math.PI, endAngle, false);
        cxt_arc.stroke();
        cxt_arc.draw();
    },

    onShareAppMessage: function () {
        return {
            title: '快来看看你今天的运动距离吧',
            path: '/pages/index/index'
        }
    }
});
