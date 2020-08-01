<template>
    <div id="box">
        <el-table
            id="tableData"
            :data="tableData"
            style="width: 80%">
            <el-table-column prop="reason" label="理由" width="180"></el-table-column>
            <el-table-column prop="sweet" label="甜蜜值" width="180"></el-table-column>
            <el-table-column prop="approval_status" label="审核状态" width="180"></el-table-column>
            <el-table-column prop="applicant" label="申请人" width="180"></el-table-column>
            <el-table-column prop="reviewer" label="审核人" width="180"></el-table-column>
            <el-table-column prop="created" label="创建时间" width="180"></el-table-column>
            <el-table-column label="操作">
            <template slot-scope="scope">
                <el-button
                size="mini"
                @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                <!-- <el-button
                size="mini"
                type="danger"
                @click="handleDelete(scope.$index, scope.row)">删除</el-button> -->
            </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
export default {
  name: 'index',
  data () {
    return {
      tableData: []
    }
  },
  mounted: function () {
    this.LoadData()
  },
  methods: {
    LoadData: function () {
      var that = this
      var data = {
        'sessionid': that.$cookies.get('sessionid')
      }
      that.$http.post(that.GLOBAL.baseURL + '/approved/', data).then(function (res) {
        console.log(res)
        if (res.data.msg === 'success') {
          that.$data.tableData = res.data.missions
        } else if (res.data.msg === 'NotExistThisUser') that.$message('未知用户')
      }, function (err) {
        console.log(err)
      })
    },
    handleEdit: function (index, row) {
      this.$router.push({
        name: 'editmission',
        params: {
          formData: row
        }
      })
    }
  }
}
</script>

<style>
#box {
  display: flex;
  justify-content: center;
  align-items: center;
}
#tableData {
  flex: unset;
  width: 10rem;
  margin-top: 2rem;
}
</style>
