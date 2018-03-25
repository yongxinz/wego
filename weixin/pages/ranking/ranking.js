var app = getApp();

Page({
    data: {
        tabs: ['全国排名', '个人数据'],
        is_ready: false,
        activeIndex: 0,
        sliderOffset: 0,
        winWidth: 0,
        winHeight: 0,
        ranks: [],
        personal: {}
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

    getPersonalData: function () {
        let that = this;
        app.helper.getApi('personal').then(function (res) {
            that.setData({personal: res.data.results})
        });
    },

    bindChange: function (e) {
        var that = this;
        that.setData({currentTab: e.detail.current});
    },

    tabClick: function (e) {
        this.setData({
            sliderOffset: e.currentTarget.offsetLeft,
            activeIndex: e.currentTarget.id
        });

        if (this.data.activeIndex === 0) {
            this.getApiData()
        } else {
            this.getPersonalData()
        }
    },

    sharePic: function (e) {
        let item = e.currentTarget.dataset.item;
        let type = e.currentTarget.dataset.type;
        let gather = e.currentTarget.dataset.gather;
        wx.navigateTo({ url: './share/share?item=' + item + '&type=' + type + '&gather=' + gather })
    }
});
