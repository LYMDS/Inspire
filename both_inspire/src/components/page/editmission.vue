<template>
    <div id="box">
        <div>
          <el-button v-show="buttonStatus.save" type="primary" v-on:click="saveMission()">保存</el-button>
          <el-button v-show="buttonStatus.commit" type="success" v-on:click="changeMissionStatus(1)">提交</el-button>
          <el-button v-show="buttonStatus.confirm" type="success" v-on:click="changeMissionStatus(2)">确认</el-button>
          <el-button v-show="buttonStatus.recall" type="warning" v-on:click="changeMissionStatus(3)">撤销</el-button>
          <el-button v-show="buttonStatus.reject" type="danger" v-on:click="changeMissionStatus(4)">驳回</el-button>
          <el-button v-show="buttonStatus.refuse" type="danger" v-on:click="changeMissionStatus(5)">拒绝</el-button>
          <el-button type="info" v-on:click="back()">返回</el-button>
        </div>
        <el-input
          id="Book"
          type="textarea"
          resize="both"
          show-word-limit
          placeholder="写下你的申请书"
          v-model="formData.reason"
          :disabled="editStatus.reason">
        </el-input>
        <p><span class="valuehead">甜蜜值</span><el-input-number v-model="formData.sweet" controls-position="right" :min="0" :disabled="editStatus.sweet"></el-input-number></p>
        <p><span class="valuehead">申请人</span><span>{{ formData.applicant }}</span></p>
        <p><span class="valuehead">审核人</span><span>{{ formData.reviewer }}</span></p>
        <p><span class="valuehead">创建时间</span><span>{{ formData.created }}</span></p>
        <el-upload
          id="UploadBox"
          :action="this.GLOBAL.baseURL + '/upfile/'"
          list-type="picture-card"
          :file-list="files"
          ref="upload"
          :on-preview="handlePictureCardPreview"
          :on-remove="handleRemove"
          :before-remove="handleBeforeRemove"
          :on-error="handleError"
          :data="uploadData"
          multiple
          :auto-upload="false"
          :limit="9"
          :disabled="editStatus.upload">
          <i class="el-icon-plus"></i>
        </el-upload>
        <el-dialog :visible.sync="dialogVisible">
          <img width="100%" :src="dialogImageUrl" alt="">
        </el-dialog>
    </div>
</template>

<script>
export default {
  name: 'index',
  data () {
    return {
      formData: {},
      files: [],
      uploadData: {},
      dialogImageUrl: '',
      dialogVisible: false,
      buttonStatus: {
        save: false,
        commit: false,
        confirm: false,
        recall: false,
        reject: false,
        refuse: false
      },
      approvalPrivilege: false, // approvalUser: true 拥有审核权限
      editStatus: {
        reason: false,
        sweet: false,
        upload: false
      }
    }
  },
  created: function () {
    this.$data.formData = this.$route.params.formData
  },
  mounted: function () {
    this.getApprovalUser()
    this.LoadFiles()
  },
  methods: {
    saveMission: function () {
      var that = this
      that.$http.post(that.GLOBAL.baseURL + '/save_mission/', that.$data.formData).then(function (res) {
        if (res.data.msg === 'success') {
          this.$refs.upload.submit()
        }
      }, function (err) {
        console.error(err)
      })
    },
    reloadData: function () {
      var that = this
      that.$http.get(that.GLOBAL.baseURL + '/getmissionbyid/?missionid=' + that.$data.formData.id).then(function (res) {
        if (res.data.msg === 'success') {
          that.$data.formData = res.data.missiondata
          that.checkButtonStatus()
        }
      }, function (err) {
        console.error(err)
      })
    },
    back: function () {
      this.$router.go(-1)
    },
    handleBeforeRemove: function (file, fileList) {
      return confirm('确定删除文件么？')
    },
    handleRemove: function (file, fileList) {
      var that = this
      that.deleteFile(file.id)
    /*
      that.$confirm('将永久删除该文件?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        that.deleteFile(file.id)
      }).catch(() => {
        that.LoadFiles()
        that.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    */
    },
    handlePictureCardPreview: function (file) {
      this.$data.dialogImageUrl = file.url
      this.$data.dialogVisible = true
    },
    deleteFile: function (id) {
      var that = this
      var data = {
        'id': id
      }
      that.$http.post(that.GLOBAL.baseURL + '/delete_file/', data).then(function (res) {
        if (res.data.msg === 'success') {
          that.$message({
            type: 'success',
            message: '删除成功!'
          })
        } else {
          that.$message({
            type: 'info',
            message: '删除失败!'
          })
        }
      }, function (err) {
        console.error(err)
      })
    },
    LoadFiles: function () {
      var that = this
      that.$data.uploadData = {
        'missionId': that.$data.formData.id,
        'fileGroupId': that.$data.formData.file_group
      }
      that.$http.get(that.GLOBAL.baseURL + '/getfilesurl/?fileGroup=' + that.$data.formData.file_group).then(function (res) {
        that.$data.files = res.data.files
      }, function (err) {
        console.log(err)
      })
    },
    checkButtonStatus: function () {
      var that = this
      // 初始化状态
      that.$data.buttonStatus = {
        save: false,
        commit: false,
        confirm: false,
        recall: false,
        reject: false,
        refuse: false
      }
      that.$data.editStatus = {
        reason: false,
        sweet: false,
        upload: false
      }
      switch (that.$data.formData.approval_status) {
        case '未提交':
          // 当前用户有审核权限
          if (that.$data.approvalPrivilege) {
            // 按钮不开放
            // 禁用所有编辑
            that.$data.editStatus.reason = true
            that.$data.editStatus.sweet = true
            that.$data.editStatus.upload = true
          } else {
            // 按钮开放保存与提交
            that.$data.buttonStatus.save = true
            that.$data.buttonStatus.commit = true
          }
          break
        case '审核中':
          // 当前用户有审核权限
          if (that.$data.approvalPrivilege) {
            // 按钮开放保存、确认和驳回
            that.$data.buttonStatus.save = true
            that.$data.buttonStatus.confirm = true
            that.$data.buttonStatus.reject = true
            // 编辑禁用理由和文件上传
            that.$data.editStatus.reason = true
            that.$data.editStatus.upload = true
          } else {
            // 按钮开放撤回
            that.$data.buttonStatus.recall = true
            // 编辑禁用所有
            that.$data.editStatus.reason = true
            that.$data.editStatus.sweet = true
            that.$data.editStatus.upload = true
          }
          break
        case '已审核':
          // 当前用户有审核权限
          if (that.$data.approvalPrivilege) {
            // 不开放按钮
            // 禁用所有编辑
            that.$data.editStatus.reason = true
            that.$data.editStatus.sweet = true
            that.$data.editStatus.upload = true
          } else {
            // 不开放按钮
            // 禁用所有编辑
            that.$data.editStatus.reason = true
            that.$data.editStatus.sweet = true
            that.$data.editStatus.upload = true
          }
          break
        case '已撤回':
          // 当前用户有审核权限
          if (that.$data.approvalPrivilege) {
            // 不开放按钮
            // 禁用所有编辑
            that.$data.editStatus.reason = true
            that.$data.editStatus.sweet = true
            that.$data.editStatus.upload = true
          } else {
            that.$data.buttonStatus.save = true
            that.$data.buttonStatus.commit = true
          }
          break
        case '已驳回':
          // 当前用户有审核权限
          if (that.$data.approvalPrivilege) {
            // 按钮不开放
            // 禁用所有编辑
            that.$data.editStatus.reason = true
            that.$data.editStatus.sweet = true
            that.$data.editStatus.upload = true
          } else {
            // 按钮开放保存与提交
            that.$data.buttonStatus.save = true
            that.$data.buttonStatus.commit = true
          }
          break
        case '已拒绝':
          // 不开放按钮
          // 禁用所有编辑
          that.$data.editStatus.reason = true
          that.$data.editStatus.sweet = true
          that.$data.editStatus.upload = true
          break
      }
    },
    getApprovalUser: function () {
      var that = this
      that.$http.get(
        that.GLOBAL.baseURL +
        '/getapprovalprivilege/?sessionid=' +
        that.$cookies.get('sessionid') +
        '&missionid=' +
        that.$data.formData.id).then(function (res) {
        that.$data.approvalPrivilege = res.data.approvalPrivilege
        that.checkButtonStatus()
      }, function (err) {
        console.log(err)
      })
    },
    changeMissionStatus: function (status) {
      var that = this
      var data = {
        'missionid': that.$data.formData.id,
        'sessionid': that.$cookies.get('sessionid'),
        'status': status
      }
      that.$http.post(that.GLOBAL.baseURL + '/change_missionstatus/', data).then(function (res) {
        if (res.data.msg === 'success') {
          that.reloadData()
          that.$message({
            type: 'success',
            message: '操作成功!'
          })
        }
      }, function (err) {
        console.error(err)
      })
    }
  }
}
</script>

<style>
#box{
  display: flex;
  flex-flow: column wrap;
  justify-content: space-around;
  align-items: center;
}
#Book{
  display: inline-block;
  width: 40rem;
  height: 15rem;
  opacity: 0.7;
}
p {
  line-height: 0rem;
  color: white;
}
.valuehead {
  margin-right: 1rem;
}
.el-message-box__message p{
  color: black;
}
</style>
