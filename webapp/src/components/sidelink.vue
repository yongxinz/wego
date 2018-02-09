<template>
    <li>
        <el-popover trigger="hover" ref="popover" placement="right" width="300">
            <ym-btnlist :items="items"></ym-btnlist>
        </el-popover>

        <el-button v-popover:popover type="primary"><i :class="icon" class="fa fa-lg fa-fw"></i> {{ title }}</el-button>
    </li>
</template>

<script>
    export default {
        props: {
            items: {
                type: Array,
                default: function () { return [] }
            },
            title: {
                type: String
            },
            icon: {
                type: String
            }
        }
    }
</script>
