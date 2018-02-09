import Vue from 'vue'

module.exports.checkStatus = function (apiResp) {
    if (apiResp.status === 500 || apiResp.status === 504) { // 服务器 500 错误
        // window.location = '/info?code=500';
        Vue.prototype.$alert('发生了点错误，请您稍后再试!', '出现错误', {
            confirmButtonText: '确定',
            callback: action => {
            }
        })
    }

    if (apiResp.status === 406) { // 服务器 406 Not Acceptable 错误
        Vue.prototype.$notify({
            title: '警告',
            message: apiResp.data.detail,
            type: 'warning'
        })
    }

    if (apiResp.status === 403) { // 403 权限错误
        if (apiResp.data.status_code === '403010' || apiResp.data.status_code === '403020') { // 非业务权限错误
            window.location = '/info';
        } else {
            Vue.prototype.$notify({
                title: '失败',
                message: apiResp.data.detail,
                type: 'warning'
            })
        }
    }

    if (apiResp.status === 200 || apiResp.status === 201) { // 200 成功
        if (apiResp.data.success_msg) { // 需要提示的成功
            Vue.prototype.$notify({
                title: '成功！',
                message: apiResp.data.success_msg,
                type: 'success'
            })
        }
    }

    if (apiResp.status === 204) { // 204 No Content
        Vue.prototype.$notify({
            title: '成功！',
            message: '删除成功！',
            type: 'success'
        })
    }
};
