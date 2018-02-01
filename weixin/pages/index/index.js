var app = getApp()

var interval;
var varName;
var ctx = wx.createCanvasContext('canvasArcCir');

Page({
    data: {
        windowWidth: 0,
        windowHeight: 0
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
    },
    onReady: function () {
        //创建并返回绘图上下文context对象。
        var cxt_arc = wx.createCanvasContext('canvasCircle');
        cxt_arc.setLineWidth(25);
        cxt_arc.setStrokeStyle('#eaeaea');
        cxt_arc.setLineCap('round');
        cxt_arc.beginPath();
        cxt_arc.arc(this.data.windowWidth / 2, this.data.windowWidth / 2, 110, 0, 2 * Math.PI, false);
        cxt_arc.stroke();
        cxt_arc.draw();
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
    }
});
