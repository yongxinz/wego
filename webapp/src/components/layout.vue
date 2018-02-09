<template>
    <div>
        <slot name="header">
            <ym-header :company_name="company_name" :username="username"></ym-header>
        </slot>
        <slot name="sidebar">
            <ym-sidebar :role="role"></ym-sidebar>
        </slot>
        <div id="main" role="main">
            <div id="content">
                <ym-tabs></ym-tabs>
                <div class="maincontent" v-if="is_permission">
                    <slot></slot>
                </div>
            </div>
        </div>
        <slot name="footer-dialog"></slot>
    </div>
</template>

<script>
    export default {
        props: {
            groups: {
                type: Array,
                default: function () {
                    return [];
                }
            }
        },

        data() {
            return {
                company_name: '',
                username: '',
                role: '',
                api_groups: []
            }
        },

        computed: {
            is_permission() {
//                if (this.api_groups.indexOf('所有') > -1) {
//                    return true
//                }
//                if (this.groups.length > 0) {
//                    let ugroups = this.groups.filter((v) => {
//                        return this.api_groups.indexOf(v) > -1
//                    });
//                    return ugroups.length > 0
//                }
                return true;
            }
        },

        activated() {
            this.$http.get(this.ym_api + '/passport/info/').then((resp) => {
                this.company_name = resp.data.company_name;
                this.username = resp.data.username;
                this.role = resp.data.role;
                this.$store.commit('setRole', resp.data.role);
            }).then((resp) => {
                if (!this.is_permission) {
                    this.$alert('您没有权限访问该内容！点击确定返回上一步！', '权限错误', {
                        confirmButtonText: '确定',
                        type: 'warning',
                        callback: action => {
                            this.$store.commit('delTab', this.ym_path.to.name);
                            this.$store.commit('setActiveName', this.ym_path.from.name);
                            this.$router.go('-1')
                        }
                    })
                }
            });

            let minHeight = 'min-height: ' + window.getComputedStyle(document.getElementById('content'), null).height;
            this.$store.commit('setMinHeight', minHeight)
        }
    };
</script>
