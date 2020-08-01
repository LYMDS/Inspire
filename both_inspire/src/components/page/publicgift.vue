<template>
<div id="publicgift">

    <el-upload
      id="UploadBox"
      :action="this.GLOBAL.baseURL + '/publicgift/'"
      list-type="picture-card"
      ref="upload"
      :on-preview="handlePictureCardPreview"
      :on-remove="handleRemove"
      :on-success="handleSuccess"
      :data="uploadData"
      :auto-upload="false"
      :limit="1">
    <i class="el-icon-plus"></i>
    </el-upload>
    <el-dialog :visible.sync="dialogVisible">
      <img width="100%" :src="dialogImageUrl" alt="">
    </el-dialog>
    <el-input
      id="Book"
      type="text"
      v-model="uploadData.title"
      show-word-limit
      placeholder="礼物描述">
    </el-input>
    <div id="sweet">
      <span class="tip">价值</span>
      <el-input-number controls-position="right" :min="0" v-model="uploadData.sweet"></el-input-number>
    </div>
    <div id="count">
      <span class="tip">数量</span>
      <el-input-number controls-position="right" :min="0" v-model="uploadData.count"></el-input-number>
    </div>
    <el-button type="success" v-on:click="publicGift()">提交</el-button>
</div>
</template>

<script>
export default {
  name: 'publicgift',
  data () {
    return {
      dialogImageUrl: '',
      dialogVisible: false,
      uploadData: {
        id: null,
        title: '',
        sweet: 0,
        count: 0,
        sessionid: this.$cookies.get('sessionid')
      }
    }
  },
  mounted: function () {
  },
  methods: {
    handlePictureCardPreview (file) {
      this.dialogImageUrl = file.url
      this.dialogVisible = true
    },
    publicGift: function () {
      console.log(this.uploadData)
      this.$refs.upload.submit()
    },
    handleSuccess (response, file, fileList) {
      this.$data.uploadData.id = response.id
    }

  }
}
</script>

<style>

</style>
