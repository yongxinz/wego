var app = getApp();

Page({
    data: {
        winWidth: 0,
        winHeight: 0,
        // tab切换
        currentTab: 0,
        ranks: []
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
    },

    onShow: function () {
        app.helper.waitUserSid(this.getApiData);
    },

    getApiData: function () {
        let that = this;
        app.helper.getApi('werun').then(function (res) {
            that.setData({ranks: res.data.results})
        });
    },

    /**
     * 滑动切换tab
     */
    bindChange: function (e) {
        var that = this;
        that.setData({currentTab: e.detail.current});
    },

    /**
     * 点击tab切换
     */
    swichNav: function (e) {
        var that = this;

        if (this.data.currentTab === e.target.dataset.current) {
            return false;
        } else {
            that.setData({
                currentTab: e.target.dataset.current
            })
        }
    }
});
