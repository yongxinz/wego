<template>
    <ym-layout>
        <el-card>
            <el-row>
                <el-button type="primary" size="small" @click="handleNew()" class="float_right">新增</el-button>
            </el-row>
            <el-table :data="apiData" stripe border>
                <el-table-column prop="type_display" label="数据类型" min-width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="min_value" label="数据分级(小)" min-width="120"
                                 show-overflow-tooltip></el-table-column>
                <el-table-column prop="max_value" label="数据分级(大)" min-width="120"
                                 show-overflow-tooltip></el-table-column>
                <el-table-column prop="reference" label="参考物" min-width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="reference_value" label="参考物数值" min-width="120"
                                 show-overflow-tooltip></el-table-column>
                <el-table-column prop="summary" label="分享文案" min-width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="created_time" label="创建时间" min-width="180" show-overflow-tooltip>
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

        <div slot="footer-dialog">
            <el-dialog title="运动数据定义" custom-class="ym-select-dialog" :visible.sync="dialogFormVisible" top="5%">
                <el-form :model="form" :rules=rules :inline="true" ref="form" :label-width="'100px'">
                    <el-row>
                        <el-form-item label="数据类型" prop="type">
                            <el-select v-model="form.type" placeholder="请选择">
                                <el-option
                                    v-for="item in type"
                                    :label="item.label"
                                    :key="item.value"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-row>
                    <el-row>
                        <el-form-item label="数据分级(小)" prop="min_value">
                            <el-input v-model.number="form.min_value" placeholder="请输入"></el-input>
                        </el-form-item>
                        <el-form-item label="数据分级(大)" prop="max_value">
                            <el-input v-model.number="form.max_value" placeholder="请输入"></el-input>
                        </el-form-item>
                    </el-row>
                    <el-row>
                        <el-form-item label="参考物" prop="reference">
                            <el-input v-model="form.reference" placeholder="请输入"></el-input>
                        </el-form-item>
                        <el-form-item label="参考物数值" prop="reference_value">
                            <el-input v-model.number="form.reference_value" placeholder="请输入"></el-input>
                        </el-form-item>
                    </el-row>
                    <el-row>
                        <el-form-item label="分享文案" prop="summary">
                            <el-input v-model="form.summary" placeholder="请输入" style="width: 300%"></el-input>
                        </el-form-item>
                    </el-row>
                    <el-row>
                        <el-form-item>
                            <el-button type="primary" @click="handleSubmit()">保存</el-button>
                        </el-form-item>
                    </el-row>
                </el-form>
            </el-dialog>
        </div>
    </ym-layout>
</template>

<script>
    import qs from 'qs'

    export default {
        data() {
            return {
                url: this.ym_api + '/define/',
                apiData: [],
                searchForm: {
                    page: 1
                },
                total: 0,
                form: {
                    type: '',
                    min_value: '',
                    max_value: '',
                    reference: '',
                    reference_value: '',
                    summary: ''
                },
                type: [],
                rules: {
                    min_value: [
                        {type: 'number', message: '数据分级(小)必须为数字值'}
                    ],
                    max_value: [
                        {type: 'number', message: '数据分级(大)必须为数字值'}
                    ],
                    reference_value: [
                        {type: 'number', message: '参考物数值必须为数字值'}
                    ]
                },
                dialogFormVisible: false,
            };
        },

        activated() {
            this.search();
            this.fetchType();
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

            handleNew() {
                this.form = {
                    id: '',
                    type: '',
                    min_value: '',
                    max_value: '',
                    reference: '',
                    reference_value: '',
                    summary: ''
                };
                this.dialogFormVisible = true
            },

            handleSubmit(ev) {
                if (this.form.id !== '') {
                    this.$http.put(this.url + this.form.id + '/', this.form).then((response) => {
                        this.dialogFormVisible = false
                    })
                } else {
                    this.$http.post(this.url, this.form).then((response) => {
                        this.dialogFormVisible = false;
                        this.search()
                    })
                }
            },

            fetchType() {
                this.$http.get(this.url + 'type/').then((response) => {
                    this.type = response.data
                })
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
