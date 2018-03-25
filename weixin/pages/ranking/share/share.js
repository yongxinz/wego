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
        content: '',
        img_url: ''
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
        ctx.setFontSize(26);
        ctx.setFillStyle("#A3A3A3");
        ctx.setTextAlign('center');
        ctx.fillText(content, 345, height);
    },

    createNewImg: function (res) {
        let that = this;
        let ctx = wx.createCanvasContext('myCanvas');
        let ctx_ = wx.createCanvasContext('myCanvasShow');
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
                ctx.drawImage(res_.tempFilePath, 0, 0, 690, 1200);
                that.drawFont(ctx, that.data.content, 820);
                that.drawFont(ctx, res.data.results.summary, 860);
                ctx.draw();

                ctx_.scale(0.5, 0.5);
                ctx_.drawImage(res_.tempFilePath, 0, 0, 690, 1200);
                that.drawFont(ctx_, that.data.content, 820);
                that.drawFont(ctx_, res.data.results.summary, 860);
                ctx_.draw();
            }
        });
    },

    savePic: function () {
        wx.canvasToTempFilePath({
            x: 0,
            y: 0,
            width: 690,
            height: 1200,
            canvasId: 'myCanvas',
            success: function (res) {
                util.savePicToAlbum(res.tempFilePath)
            }
        });
    }
});