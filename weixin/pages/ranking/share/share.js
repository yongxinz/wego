import util from '../../../utils/util'

const app = getApp();

Page({
    data: {
        windowWidth: 0,
        windowHeight: 0,
        contentHeight: 0,
        thinkList: [],
        footer: '',
        offset: 0,
        lineHeight: 30,
        content: ''
    },

    onLoad: function (options) {
        let that = this;
        that.setData({options: options});
        if (options.gather === 'day') {
            that.setData({content: '今天我走了 ' + options.item + ' 步,'});
        } else if (options.gather === 'week') {
            that.setData({content: '本周我走了 ' + options.item + ' 步,'});
        } else if (options.gather === 'month') {
            that.setData({content: '本月我走了 ' + options.item + ' 步,'});
        }
        wx.getSystemInfo({
            success: function (res) {
                that.setData({
                    windowWidth: res.windowWidth,
                    windowHeight: res.windowHeight,
                    offset: (res.windowWidth - 304) / 2
                });
            }
        });
    },

    onShow: function () {
        app.helper.waitUserSid(this.getApiData)
    },

    getApiData: function () {
        let that = this;

        wx.showLoading({ title: '海报生成中...' });
        app.helper.getApi('summary', that.data.options).then(function (res) {
            that.createNewImg(res)
        })
    },

    drawFont: function (ctx, content, height) {
        ctx.setFontSize(13);
        ctx.setFillStyle("#A3A3A3");
        ctx.setTextAlign('center');
        ctx.fillText(content, 172, height);
    },

    createNewImg: function (res) {
        let that = this;
        let ctx = wx.createCanvasContext('myCanvas');
        if (res.data.results.summary === '') {
            res.data.results.summary = '如果帅可以当饭吃，我可以养活十万人'
        }

        wx.downloadFile({
            url: app.helper.getUrl('summary_pic') + '?pk=' + res.data.results.pk,
            header: {
                'Authorization': app.config.gData.userSid
            },
            success: function (res_) {
                wx.hideLoading();
                ctx.drawImage(res_.tempFilePath, 0, 0, 345, 600);
                that.drawFont(ctx, that.data.content, 410);
                that.drawFont(ctx, res.data.results.summary, 430);
                ctx.draw();
            }
        });
    },

    savePic: function () {
        wx.canvasToTempFilePath({
            x: 0,
            y: 0,
            width: 345,
            height: 600,
            canvasId: 'myCanvas',
            success: function (res) {
                util.savePicToAlbum(res.tempFilePath)
            }
        });
    }
});