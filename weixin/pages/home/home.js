const app = getApp();

Page({
    data: {
        gData: null,
        results: {}
    },

    onLoad: function () {

    },

    onShow: function () {
        app.helper.waitUserSid(this.getApiData);
    },

    updateUsers: function () {
        let that = this;

        app.helper.putApi('users', that.data.gData, this.data.results.id + '/nickname/').then(function (res) {
            console.log(res)
        })
    },

    getApiData: function () {
        let that = this;

        app.helper.getApi('users').then(function (res) {
            that.setData({results: res.data.results[0]});
            that.setData({'gData.mobile': res.data.results[0].mobile});
        })
    },

    onGotUserInfo: function(e) {
        let that = this;

        app.config.gData.userInfo = e.detail.userInfo;
        that.setData({'gData.userInfo': app.config.gData.userInfo});
        that.setData({'results.nickname': app.config.gData.userInfo.nickName});
        that.setData({'results.avatar_url': app.config.gData.userInfo.avatarUrl});
        app.helper.waitUserSid(that.updateUsers);
    },

    updateTarget(e) {
        wx.navigateTo({url: e.currentTarget.dataset.url})
    },

    cancelBind: function () {
        let that = this;
        app.helper.getApi('cancel').then(function (res) {
            if (res.data.status) {
                app.config.gData.mobile = '';
                that.setData({'gData.mobile': app.config.gData.mobile});
                wx.redirectTo({url: '/pages/login/login'})
            }
        })
    }
});
