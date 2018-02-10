<template>
    <ym-layout>
        <el-card>
            <el-table :data="apiData" stripe border>
                <el-table-column prop="in_no" label="入库单号" width="190" show-overflow-tooltip>
                    <template slot-scope="scope">
                        <span>{{ scope.row.in_no }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="in_no" label="总计" width="160" show-overflow-tooltip>
                    <template slot-scope="scope" style="font-size: 10px; color: dimgray;">
                        <span>{{ scope.row.total_package }} 包 , {{ scope.row.total_volume }} m³</span>
                    </template>
                </el-table-column>
                <el-table-column prop="dealer_name" label="经销商" min-width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="supplier_name" label="供货商" min-width="120"
                                 show-overflow-tooltip></el-table-column>
                <el-table-column prop="contract_no" label="合同号" min-width="180" show-overflow-tooltip></el-table-column>
                <el-table-column prop="bill_no" label="提单号" min-width="180" show-overflow-tooltip></el-table-column>
                <el-table-column prop="depot_name" label="仓库" min-width="150" show-overflow-tooltip></el-table-column>
                <el-table-column prop="pdbrand_pdbrand" label="品牌" min-width="120"
                                 show-overflow-tooltip></el-table-column>
                <el-table-column prop="operator_name" label="制单员" min-width="80"
                                 show-overflow-tooltip></el-table-column>
                <el-table-column prop="keeper_name" label="仓管员" min-width="80" show-overflow-tooltip></el-table-column>
                <el-table-column prop="in_time" label="入库时间" min-width="170">
                    <template slot-scope="scope">
                        <div v-if="scope.row.in_time">
                            {{ scope.row.in_time | moment }}
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="remark_in" label="备注" min-width="120" show-overflow-tooltip></el-table-column>
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
                url: this.ym_api + '/users/',
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
            },
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
