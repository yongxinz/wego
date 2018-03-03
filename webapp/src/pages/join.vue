<template>
    <div>
        <div id="loginmain">
            <el-row>
                <el-col>
                    <el-card :body-style="{ padding: '20px' }">
                        <div slot="header" class="clearfix">
                            <span id="logo"><img src="../assets/logo.png" alt="WEGO"> </span>
                            <div class="pull-right tel400">技术支持，微信咨询：zhangyx6a</div>
                        </div>
                        <el-form>
                            <el-alert :title="result.msg" type="error" :closable="false" v-if="result.msg" show-icon></el-alert>
                            <div style="margin-top: 15px;" class="login captcha">
                                <el-input placeholder="请输入您常用的手机号，并确认其真实有效，以便接收验证短信" v-model="baseForm.form.mobile">
                                    <template slot="prepend">手机号：</template>
                                </el-input>
                            </div>
                            <div style="margin-top: 15px;" class="login captcha">
                                <el-input placeholder="请设置您的密码：至少8位、至少有一位数字和字母" type="password" v-model="baseForm.form.password">
                                    <template slot="prepend">密码：</template>
                                </el-input>
                            </div>
                            <div style="margin-top: 15px;" class="login">
                                <el-input placeholder="请输入图片验证码中显示的4位数字, 点击验证码图片可刷新" v-model="baseForm.form.imgcode">
                                    <template slot="prepend">验证码：</template>
                                    <template slot="append">
                                        <img :src="baseForm.imgurl" @click="getCaptcha" style="height: 34px">
                                    </template>
                                </el-input>
                            </div>
                            <el-form-item style="margin-top: 15px;">
                                <el-button type="primary" @click="onSubmit">{{ baseForm.btn.msg}}

                                </el-button>
                                <div class="pull-right">
                                    <router-link :to="{path: 'login'}">
                                        <el-button type="text">已有账户？</el-button>
                                    </router-link>
                                </div>
                            </el-form-item>
                        </el-form>
                    </el-card>
                </el-col>
            </el-row>
        </div>
        <el-dialog title="短信验证码已发送到手机！" :visible="baseForm.form.dialogSMS">
            <el-form>
                <el-form-item label="请输入短信验证码">
                    <el-input v-model="baseForm.form.smscode" auto-complete="off"></el-input>
                </el-form-item>
            </el-form>
            <div>{{ result.msg }}</div>
            <div slot="footer" class="dialog-footer">
                <el-button @click="baseForm.form.dialogSMS = false">取 消</el-button>
                <el-button type="primary" @click="checkSMS">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        data () {
            return {
                baseForm: {
                    btn: {msg: '注册'},
                    form: {dialogSMS: false},
                    imgurl: ''
                },
                result: {
                    errors: '',
                    msg: ''
                }
            }
        },

        activated: function () {
            if (this.$route.query.action === 'reset') {
                this.baseForm.btn.msg = '重置密码'
            } else {
                this.baseForm.btn.msg = '注册'
            }
            this.getCaptcha()
        },

        methods: {
            onSubmit() {
                this.$http.post('/api/passport/join/', this.baseForm.form).then((response) => {
                    if (response.data.status) {
                        this.result.msg = '';
                        this.baseForm.form.dialogSMS = true
                    } else {
                        this.result.msg = response.data.msg;
                        if (response.data.status_code === 500200) {
                            this.getCaptcha()
                        }
                    }
                })
            },

            checkSMS() {
                this.$http.post('/api/passport/join/', this.baseForm.form).then((response) => {
                    if (response.data.status) {
                        window.localStorage.setItem('userhashid', response.data.userhashid);
                        this.$http.defaults.headers.common['Authorization'] = response.data.userhashid;
                        this.baseForm.form.dialogSMS = false;
                        this.$router.replace('/info')
                    } else {
                        this.result.msg = response.data.msg;
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
