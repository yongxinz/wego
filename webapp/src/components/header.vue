<template>
    <header id="header">

        <div id="logo-group">
            <span id="logo"><img src="../assets/logo.png" alt="wego"> </span>
        </div>

        <div class="hidden-xs" style="color: #000; margin-left: 10px">
            <h1>WEGO运动运营管理平台</h1>
        </div>

        <div class="pull-right" v-if="username">
            <el-dropdown style="color: #000; line-height: 50px; font-size: 120%; cursor: pointer"
                         @command="handleCommand" trigger="click">
                <span class="el-dropdown-link">
                    {{ username }}
                    <i class="el-icon-caret-bottom el-icon--right" style="font-size: 50%"></i>
                </span>
                <el-dropdown-menu slot="dropdown" style="width: 180px">
                    <el-dropdown-item divided command="logout">退出</el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </div>

    </header>
</template>

<script>
    export default {
        data() {
            return {

            }
        },

        props: {
            username: {
                default: function () {
                    return '';
                }
            }
        },

        created() {
        },

        methods: {
            handleCommand(command) {
                if (command === 'logout') {
                    this.logout()
                }
            },

            logout() {
                window.localStorage.removeItem('userhashid');
                window.location = '/login';
            }
        }
    }
</script>

<style>
    .total-form .el-form-item {
        margin-bottom: 0;
    }

    .quick-form .el-form-item__label {
        margin-bottom: 0;
        color: white;
    }

    .quick-form .el-form-item__content {
        line-height: inherit;
    }

    .select-item .el-input .el-input__inner {
        height: 30px;
        font-size: 13px;
    }
</style>
