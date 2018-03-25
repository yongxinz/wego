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
        lineHeight: 30
    },

    onLoad: function (options) {
        let that = this;
        that.setData({options: options});
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

    drawSquare: function (ctx, height) {
        ctx.setFontSize(24);
        ctx.rect(0, 50, this.data.windowWidth, height);
        ctx.setFillStyle("#f5f6fd");
        ctx.fill()
    },

    drawFont: function (ctx, content, height) {
        ctx.setFontSize(16);
        ctx.setFillStyle("#484a3d");
        ctx.fillText(content, this.data.offset, height);
    },

    drawLine: function (ctx, height) {
        ctx.beginPath();
        ctx.moveTo(this.data.offset, height);
        ctx.lineTo(this.data.windowWidth - this.data.offset, height);
        ctx.stroke('#eee');
        ctx.closePath();
    },

    createNewImg: function (res) {
        let ctx = wx.createCanvasContext('myCanvas');

        wx.downloadFile({
            url: app.helper.getUrl('summary_pic') + '?pk=' + res.data.results.pk,
            header: {
                'Authorization': app.config.gData.userSid
            },
            success: function (res) {
                wx.hideLoading();
                ctx.drawImage(res.tempFilePath, 0, 0, 345, 600);
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