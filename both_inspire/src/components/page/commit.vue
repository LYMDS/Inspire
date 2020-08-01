<template>
<div id="commit">
    <el-input
        id="Book"
        type="textarea"
        resize="both"
        show-word-limit
        placeholder="写下你的申请书"
        v-model="formdata.context">
    </el-input>
    <el-upload
        id="UploadBox"
        :action="this.GLOBAL.baseURL + '/upfile/'"
        list-type="picture-card"
        ref="upload"
        :on-preview="handlePictureCardPreview"
        :on-remove="handleRemove"
        :on-error="handleError"
        :data="uploadData"
        multiple
        :auto-upload="false"
        :limit="9">
    <i class="el-icon-plus"></i>
    </el-upload>
    <el-dialog :visible.sync="dialogVisible">
    <img width="100%" :src="dialogImageUrl" alt="">
    </el-dialog>
    <div id="sweet">
        <span class="tip">申请甜蜜值:</span>
        <el-input-number v-model="formdata.sweet" controls-position="right" :min="0"></el-input-number>
    </div>
    <el-button type="success" v-on:click="commitMission()">提交</el-button>
</div>
</template>

<script>
export default {
  name: 'commit',
  data () {
    return {
      dialogImageUrl: '',
      dialogVisible: false,
      formdata: {
        missionid: null,
        context: '',
        sweet: 0,
        sessionid: this.$cookies.get('sessionid')
      },
      uploadData: {
        'missionId': '',
        'fileGroupId': ''
      }
    }
  },
  mounted: function () {
  },
  methods: {
    handleRemove (file, fileList) {
      console.log(file, fileList)
    },
    handlePictureCardPreview (file) {
      this.dialogImageUrl = file.url
      this.dialogVisible = true
    },
    handleError (err, file, fileList) {
      console.log('上传失败')
      console.log(err)
      console.log(file)
      console.log(fileList)
    },
    commitMission: function () {
      var that = this
      that.$http.post(that.GLOBAL.baseURL + '/create_mission/', that.$data.formdata).then(function (res) {
        that.$data.formdata.missionid = res.data.missionId
        that.$data.uploadData['missionId'] = res.data.missionId
        that.$data.uploadData['fileGroupId'] = res.data.fileGroupId
        that.$refs.upload.submit()
      }, function (err) {
        console.log(err)
      })
    }
  }
}
</script>

<style>
#commit{
  display: flex;
  flex-flow: column wrap;
  justify-content: space-around;
  align-items: center;
}
#UploadBox{
  margin-top: 2rem;
  opacity: 0.7 ;
}
#Book{
  display: inline-block;
  width: 80rem;
  height: 20rem;
  opacity: 0.7;
}
#sweet{
  height: 3rem;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.tip{
  font-size: 1.2rem;
  color: rgb(186, 224, 103);
  opacity: 0.7;
}
.el-input-number{
  opacity: 0.7;
}
</style>
