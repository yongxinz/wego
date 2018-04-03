const app = getApp();

Page({
    data: {
        toastMessage: '',
        target: 6000
    },

    onLoad: function (options) {
        if (options) {
            this.setData({
                target: options.target, id: options.id
            });
        }
    },

    targetInput: function (e) {
        this.setData({target: e.detail.value})
    },

    targetSubmit: function () {
        if (this.data.target === '') {
            app.helper.setToast(this, '别慌！填好目标再保存。')
        } else if (this.data.target > 99999) {
            app.helper.setToast(this, '别闹！是不是对自己太自信了。')
        } else {
            app.helper.putApi(
                'users', {'target': this.data.target}, this.data.id + '/target/'
            ).then(function (res) {
                wx.navigateBack()
            })
        }
    }
});
