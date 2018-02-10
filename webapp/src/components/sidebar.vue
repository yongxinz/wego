<template>
    <aside id="left-panel">
        <nav class="youmu" style="height: 95%">
            <ul>
                <li>
                    <router-link to="/">
                        <el-button><i class="fa fa-lg fa-fw fa-home"></i> 首页</el-button>
                    </router-link>
                </li>

                <ym-sidelink title="用户" :items="getNavs('001')" icon="fa-align-justify"></ym-sidelink>
            </ul>
        </nav>
    </aside>
</template>

<script>
    import routes from '../routes'

    export default {
        data() {
            return {
                items: routes
            }
        },

        props: {
            role: {
                default: function () {
                    return '';
                }
            }
        },

        methods: {
            getNavs: function (type) {
                return routes.filter(function (element, index, array) {
                    if (element.sideShow === false) {
                        return false
                    } else {
                        return (element.name.indexOf(this) === 0)
                    }
                }, type)
            }
        }
    }
</script>
<style>
    .popover-ym div {
        float: left;
        text-align: center;
    }
</style>
