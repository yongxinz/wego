var app = getApp();

Page({
    data: {
        tabs: ['个人数据', '全国排名'],
        activeIndex: 0,
        sliderOffset: 0,
        winWidth: 0,
        winHeight: 0,
        ranks: [],
        personal: {},
        gData: null,
        results: {}
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
        app.helper.waitUserSid(this.getPersonalData);
    },

    getApiData: function () {
        let that = this;
        app.helper.getApi('ranking').then(function (res) {
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
            app.helper.waitUserSid(this.getPersonalData);
        } else {
            app.helper.waitUserSid(this.getApiData);
        }
    },

    sharePic: function (e) {
        let item = e.currentTarget.dataset.item;
        let type = e.currentTarget.dataset.type;
        let gather = e.currentTarget.dataset.gather;
        wx.navigateTo({ url: './share/share?item=' + item + '&type=' + type + '&gather=' + gather })
    }
});
