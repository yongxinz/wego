var app = getApp();

Page({
    data: {
        tabs: ['全国排名', '个人数据'],
        is_ready: false,
        activeIndex: 0,
        sliderOffset: 0,
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
            let ranks = [];
            for (let i = 0; i < 10; i++) {
                ranks.push(res.data.results[0])
            }
            that.setData({ranks: ranks})
        });
    },

    /**
     * 滑动切换tab
     */
    bindChange: function (e) {
        var that = this;
        that.setData({currentTab: e.detail.current});
    },

    tabClick: function (e) {
        this.setData({
            sliderOffset: e.currentTarget.offsetLeft,
            activeIndex: e.currentTarget.id
        });
    }
});
