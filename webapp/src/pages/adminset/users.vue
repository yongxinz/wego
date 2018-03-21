<template>
    <ym-layout>
        <el-card>
            <el-table :data="apiData" stripe border>
                <el-table-column prop="mobile" label="注册电话" min-width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="nickname" label="昵称" min-width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="created_time" label="注册时间" min-width="180" show-overflow-tooltip>
                    <template slot-scope="scope">
                        <div>
                            {{ scope.row.created_time|moment }}
                        </div>
                    </template>
                </el-table-column>
            </el-table>

            <el-pagination
                @current-change="handleCurrentChange"
                :total="total"
                :page-size="15"
                layout="total, prev, pager, next, jumper">
            </el-pagination>
        </el-card>
    </ym-layout>
</template>

<script>
    import qs from 'qs'

    export default {
        data() {
            return {
                url: this.ym_api + '/users/all/',
                apiData: [],
                searchForm: {
                    page: 1
                },
                total: 0
            };
        },

        activated() {
            this.search()
        },

        methods: {
            search() {
                let queryStr = qs.stringify(this.searchForm, {arrayFormat: 'repeat'});
                this.$http.get(this.url + '?' + queryStr).then((response) => {
                    this.apiData = response.data.results;
                    this.total = response.data.count;
                }).catch((error) => {
                    if (error.response.data.detail === '无效页面。') {
                        this.handleCurrentChange(1)
                    }
                })
            },

            handleCurrentChange(val) {
                this.searchForm.page = val;
                this.search()
            }
        }
    }
</script>

<style>
    .el-form .el-form-item {
        margin-bottom: 20px;
    }

    .in_list_input > .el-input__inner {
        height: 35px;
    }

    .el-date-editor--datetimerange.el-input {
        width: 300px;
        min-width: 200px;
    }
</style>
