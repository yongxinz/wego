<template>
    <ym-layout>
        <el-card>
            <el-table :data="apiData" stripe border>
                <el-table-column prop="title" label="活动" min-width="200"
                                 show-overflow-tooltip></el-table-column>
                <el-table-column prop="start_time" label="开始时间" min-width="180" show-overflow-tooltip>
                    <template slot-scope="scope">
                        <div>
                            {{ scope.row.start_time|moment }}
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="end_time" label="结束时间" min-width="180" show-overflow-tooltip>
                    <template slot-scope="scope">
                        <div>
                            {{ scope.row.end_time|moment }}
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="created_time" label="创建时间" min-width="180" show-overflow-tooltip>
                    <template slot-scope="scope">
                        <div>
                            {{ scope.row.created_time|moment }}
                        </div>
                    </template>
                </el-table-column>
                <el-table-column label="操作" fixed="right" min-width="100">
                    <template slot-scope="scope">
                        <el-button size="small" type="primary" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
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
                url: this.ym_api + '/activity/list/',
                apiData: [],
                searchForm: {
                    page: 1
                },
                total: 0
            };
        },

        activated() {
            this.search();
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
