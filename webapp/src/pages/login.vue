<template>
    <div id="loginmain" v-if="baseForm.imgurl">
        <el-row>
            <el-col>
                <el-card :body-style="{ padding: '20px' }">
                    <div slot="header" class="clearfix">
                        <span id="logo"><img src="../assets/logo.png" alt="WEGO"> </span>
                        <div class="pull-right tel400">技术支持，微信咨询：zhangyx6a</div>
                    </div>
                    <el-form>
                        <el-alert :title="result.msg" type="error" :closable="false" v-if="result.msg" show-icon></el-alert>
                        <div style="margin-top: 15px;">
                            <el-input
                                    name="username" class="login captcha"
                                    placeholder="请输入您注册时使用的手机号"
                                    v-model="baseForm.form.mobile">
                                <template slot="prepend">手机号：</template>
                            </el-input>
                        </div>
                        <div style="margin-top: 15px;">
                            <el-input
                                    name="password" type="password"
                                    placeholder="请输入密码" class="login captcha"
                                    v-model="baseForm.form.password">
                                <template slot="prepend">密&emsp;码：</template>
                            </el-input>
                        </div>
                        <div style="margin-top: 15px;">
                            <el-input placeholder="请输入图片验证码中显示的4位数字, 点击验证码图片可刷新"
                                      v-model="baseForm.form.imgcode" class="login">
                                <template slot="prepend">验证码：</template>
                                <template slot="append">
                                    <img :src="baseForm.imgurl" @click="getCaptcha" style="height: 34px">
                                </template>
                            </el-input>
                        </div>
                        <el-form-item style="margin-top: 15px;">
                            <el-button type="primary" @click="onSubmit">登录</el-button>
                            <div class="pull-right">
                                <router-link :to="{path: 'join'}">
                                    <el-button type="text">没有账户？</el-button>
                                </router-link>
                            </div>
                            <div class="pull-right">
                                <router-link :to="{path: 'join', query: { action: 'reset' }}">
                                    <el-button type="text">忘记密码？</el-button>
                                </router-link>
                            </div>
                        </el-form-item>
                    </el-form>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    export default {
        data () {
            return {
                baseForm: {
                    form: {},
                    imgurl: ''
                },
                result: {
                    errors: '',
                    msg: ''
                }
            }
        },

        activated: function() {
            this.getCaptcha()
        },

        methods: {
            onSubmit() {
                this.$http.post('/api/passport/login/', this.baseForm.form).then((response) => {
                    if (response.data.status) {
                        window.localStorage.setItem('userhashid', response.data.userhashid);
                        this.$http.defaults.headers.common['Authorization'] = response.data.userhashid;
                        this.$router.replace('/info')
                    } else {
                        this.result.msg = response.data.msg;
                        if (response.data.status_code === 500200) { // 图片验证码错误，刷新验证码
                            this.getCaptcha()
                        }
                    }
                })
            },

            getCaptcha() {
                this.$http.get('/api/passport/captcha/refresh/').then((response) => {
                    this.baseForm.imgurl = response.data.url;
                    this.baseForm.form.imgkey = response.data.key;
                    this.baseForm.form.imgcode = ''
                })
            }
        }
    }
</script>

<style>

</style>
