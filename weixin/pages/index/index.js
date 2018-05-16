var util = require('../../utils/util.js');
var wxCharts = require('../../utils/wxcharts.js');
var lineChart = null;

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
        that.drawCircle(cxt_arc, '#eeeeee', 3.5 * Math.PI, 'canvasCircle');

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
                that.drawCircle(cxt_arc, '#d81e06', (2 * targetFlag + 1.5) * Math.PI, 'canvasArcCir')
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

    bindCheck: function (e) {
        var id = e.target.dataset.id;

        if (id === '') {
            this.setData({current: 1})
        } else {
            for (let i = 0; i < this.data.apiData.length; i++) {
                if (id === this.data.apiData[i].id) {
                    this.setData({current: i + 1})
                }
            }
        }
    },

    bindChange: function (e) {
        var that = this;
        var current = e.detail.current;
        if (current > 0) {
            app.helper.getApi('activity_detail', {'activity': that.data.apiData[current-1].id}).then(function (res) {
                var image_url = app.config.baseURL + app.config.apiMap.get_title_pic + '?pk=' + res.data.results.pic_id;
                that.setData({image_url: image_url});
                that.setData({detail: res.data.results});

                if (that.data.apiData[current-1].type === 'W' && res.data.results.dates.length > 0) {
                    that.initChart(res.data.results.dates, res.data.results.steps);
                    setTimeout( function () {
                        wx.canvasToTempFilePath({
                            canvasId: 'lineCanvas',
                            success: function (res) {
                                that.setData({image_line_canvas: res.tempFilePath});
                            }
                        });
                    }, 1100);
                }
            });
        }
    },

    activityContent: function (e) {
        var reward = e.target.dataset.item.reward;
        var type = e.target.dataset.item.type;

        if (type === 'D') {
            var d1 = new Date();
            var d2 = new Date(d1);
            var d3 = new Date(d1);
            d2.setDate(d1.getDate()+1);
            d3.setDate(d1.getDate()+2);

            var start_time = util.formatFullTime(d2) + ' 00:00:00';
            var end_time = util.formatFullTime(d2) + ' 24:00:00';

            var content = '活动时间：' + util.formatTime(d2) + ' 00:00~24:00。挑战需要支付 ' + reward + ' 元钱，挑战成功后，奖金会在 '
                + util.formatTime(d3) + ' 上午 10:00 发放到微信零钱。记得在 10:00 点之前同步步数哦。'
        } else if (e.target.dataset.item.type === 'W') {
            d1 = new Date();
            d2 = new Date(d1);
            d3 = new Date(d1);
            var d4 = new Date(d1);
            d2.setDate(d1.getDate()+1);
            d3.setDate(d1.getDate()+7);
            d4.setDate(d1.getDate()+8);

            start_time = util.formatFullTime(d2) + ' 00:00:00';
            end_time = util.formatFullTime(d3) + ' 24:00:00';

            content = '活动时间：' + util.formatTime(d2) + ' 00:00~' + util.formatTime(d3) + ' 24:00'
                + '挑战需要支付 ' + reward + ' 元钱，挑战成功后，奖金会在 '
                + util.formatTime(d4) + ' 上午 10:00 发放到微信零钱。记得在 10:00 点之前同步步数哦。'
        }

        return {'start_time': start_time, 'end_time': end_time, 'content': content};
    },

    bindJoinConfirm: function (e) {
        let id = e.target.dataset.item.id;
        let user = e.target.dataset.item.user;
        let status = e.target.dataset.status;

        let content = this.activityContent(e);

        app.helper.getApi('is_join', {'start_time': new Date(content.start_time).toISOString()}).then(function (res) {
            if (res.data.results.length > 0) {
                if (res.data.results[0].status === 'OBS') {
                    app.helper.putApi('activity_join', {'status': status}, res.data.results[0].id + '/join/').then(function (res) {
                        wx.showToast({title: '参加成功', icon: 'success', duration: 1000})
                    });
                } else {
                    wx.showToast({title: '已经参加了哦~', icon: 'none', duration: 2000})
                }
            } else {
                wx.showModal({
                    title: '活动信息',
                    content: content.content,
                    confirmText: "确定",
                    cancelText: "取消",
                    success: function (res_) {
                        if (res_.confirm) {
                            let form = {'user': user, 'activity': id, 'status': status,
                                        'start_time': new Date(content.start_time), 'end_time': new Date(content.end_time)};

                            app.helper.postApi('activity_join', form).then(function (res) {
                                wx.showToast({title: '参加成功', icon: 'success', duration: 1000})
                            })
                        }
                    }
                });
            }
        });
    },

    initChart: function (cate, d1) {
        lineChart = new wxCharts({
            canvasId: 'lineCanvas',
            type: 'line',
            categories: cate,
            series: [{
                name: '步数',
                data: d1
            }],
            xAxis: {
                disableGrid: true
            },
            yAxis: {
                title: '',
                min: 0,
                disabled: true
            },
            width: this.data.windowWidth-20,
            height: 180,
            background: '#f5f5f5',
            dataPointShape: true,
            legend: false,
            extra: {
                lineStyle: 'straight'
            }
        })
    },

    openActivityInfoAlert: function () {
        wx.showModal({
            content: '弹窗内容，告知当前状态、信息和解决方法，描述文字尽量控制在三行内',
            showCancel: false,
            success: function (res) {
                if (res.confirm) {
                    console.log('用户点击确定')
                }
            }
        });
    },

    bindFabulous: function (e) {
        let activity_join = e.target.dataset.activity_join;
        let user_receive = e.target.dataset.user_receive;
        let index = e.target.dataset.index;

        let that = this;
        let detail = that.data.detail;

        app.helper.postApi('fabulous', {'activity_join': activity_join, 'user_receive': user_receive}).then(function (res) {
            detail.res[index].is_fabulous = true;
            detail.res[index].fabulous += 1;
            that.setData({detail: detail})
        })
    },

    drawCircle: function (cxt_arc, color, endAngle, canvasId) {
        cxt_arc.setLineWidth(25);
        cxt_arc.setStrokeStyle(color);
        cxt_arc.setLineCap('round');
        cxt_arc.beginPath();
        cxt_arc.arc((this.data.windowWidth - 20) / 2, (this.data.windowWidth - 20) / 2 - 71 + 57.5, this.data.radius, 1.5 * Math.PI, endAngle, false);
        cxt_arc.stroke();
        cxt_arc.draw();

        let that = this;
        if (canvasId === 'canvasCircle') {
            setTimeout( function () {
                wx.canvasToTempFilePath({
                    canvasId: canvasId,
                    success: function (res) {
                        that.setData({canvasCircle: res.tempFilePath});
                    }
                });
            }, 1000);
        } else {
            setTimeout( function () {
                wx.canvasToTempFilePath({
                    canvasId: canvasId,
                    success: function (res) {
                        that.setData({canvasArcCir: res.tempFilePath});
                    }
                });
            }, 1000);
        }
    },

    onShareAppMessage: function () {
        return {
            title: '快来看看你今天的运动距离吧',
            path: '/pages/index/index'
        }
    }
});
