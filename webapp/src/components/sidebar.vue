<template>
    <aside id="left-panel">
        <nav class="youmu" style="height: 95%">
            <ul>
                <li>
                    <router-link to="/">
                        <el-button><i class="fa fa-lg fa-fw fa-home"></i> 首页</el-button>
                    </router-link>
                </li>

                <ym-sidelink title="入库" :items="getNavs('001')" icon="fa-indent"></ym-sidelink>
                <ym-sidelink title="出库" :items="getNavs('002')" icon="fa-outdent"></ym-sidelink>
                <ym-sidelink title="库存" :items="getNavs('003')" icon="fa-align-justify"></ym-sidelink>
                <template v-if="$store.state.role == 'AD' || $store.state.role == 'CU'">
                    <ym-sidelink title="盘点" :items="getNavs('004')" icon="fa-bar-chart-o"></ym-sidelink>
                    <ym-sidelink title="仓租" :items="getNavs('005')" icon="fa-th"></ym-sidelink>
                    <ym-sidelink title="设置" :items="getNavs('006')" icon="fa-gear"></ym-sidelink>
                </template>
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
