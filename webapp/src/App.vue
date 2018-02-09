<template>
    <keep-alive><router-view></router-view></keep-alive>
</template>

<script>
    export default {
        data () {
            return {
                isLogin: Boolean(window.localStorage.getItem('userhashid'))
            }
        }
    }
</script>

<style lang="css">
    @import '../node_modules/element-ui/lib/theme-chalk/index.css';
    @import 'assets/css/font-awesome.min.css';
    @import 'assets/css/bs.css';
    @import 'assets/main.css';
</style>
