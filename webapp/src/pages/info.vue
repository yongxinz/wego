<template>
    <div v-if="msg">
        <div id="loginmain">
            <el-row>
                <el-col>
                    <el-card :body-style="{ padding: '20px' }">
                        <div slot="header" class="clearfix">
                            <span id="logo"><img src="../assets/logo.png" alt="云仓ERP"> </span>
                            <div class="pull-right tel400">咨询热线：400-723-0868</div>
                        </div>
                        <el-form>
                            <el-alert :title="msg" type="error" :closable="false" :description="msgd"></el-alert>
                            <el-form-item style="margin-top: 80px; text-align: center;">
                                <el-button type="primary" @click="reLogin">重新登陆</el-button>
                            </el-form-item>
                        </el-form>
                    </el-card>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
    export default {
        data () {
            return {
                msg: '',
                msgd: ''
            }
        },

        activated: function () {
            if (this.$route.query.code === '500') {
                this.msg = '木头哥出小差了! ';
                this.msgd = '请您稍后再来，或联系我们: 400-723-0868'
            } else {
                this.checkStatus()
            }
        },

        methods: {
            reLogin() {
                this.$router.replace('/login')
            },
            reIn() {
                window.location = '/'
            },
            checkStatus() {
                this.$http.get('/api/passport/info/').then((response) => {
                    if (response.data.status) {
                        window.location = '/'
                    } else {
                        this.msg = response.data.msg
                    }
                })
            }
        }
    }
</script>
