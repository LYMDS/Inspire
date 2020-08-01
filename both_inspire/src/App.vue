<template>
  <div :id="is_login ? 'app': 'login_app'">
    <el-menu id="menu" v-if="is_login"
    :default-active="activeIndex2"
    class="el-menu-demo"
    mode="horizontal"
    @select="handleSelect"
    background-color="#545c64"
    text-color="#fff"
    active-text-color="#ffd04b"
    router=true>
      <el-menu-item index="index" route="/">首页</el-menu-item>
      <el-menu-item index="commit">提交任务</el-menu-item>
      <el-submenu index="reward">
        <template slot="title">奖励中心</template>
        <el-menu-item index="publicgift">发布奖励</el-menu-item>
        <el-menu-item index="mygift">我的奖励</el-menu-item>
        <el-menu-item index="exchangeable">Ta的奖励</el-menu-item>
      </el-submenu>
      <el-submenu index="approval">
        <template slot="title">审核中心</template>
        <el-menu-item index="approving">待审核</el-menu-item>
        <el-menu-item index="approved">已审核</el-menu-item>
        <el-menu-item index="sendbymyself">我发起的</el-menu-item>
      </el-submenu>

      <el-popover
        popper-class="elPopover"
        effect="dark"
        placement="bottom-end"
        width="80"
        trigger="click"
        >
        <div id='fullname' class="InPopoverContext">
          <div>
            {{ name }}
          </div>
        </div>
        <div class="heart">
          <div>{{ sweet }}</div>
        </div>
        <el-button class="InPopoverContext" type="success" @click="dialogChangeHeadImgVisible = true">更换头像<i class="el-icon-upload el-icon--right"></i></el-button>
        <el-button class="InPopoverContext" type="danger" @click="quitLogin()" style="margin-left: 0rem">退出登录<i class="el-icon-bicycle el-icon--right"></i></el-button>
        <img id='Cabecera' :src="headImgUrl" slot="reference"/>
      </el-popover>

    </el-menu>
    <router-view v-if="is_login"/>
    <div v-if="!is_login" id="login_box">
      <div id="title">激励计划</div>
      <el-input class="inputUserName" v-model="username" placeholder="你的用户名"></el-input>
      <el-input class="inputPassWord" v-model="password" placeholder="密码" type="password"></el-input>
      <el-button class="btn" type="primary" icon="el-icon-success" v-on:click="login()">登录</el-button>
    </div>

    <el-dialog v-if="is_login" title="更换头像" :visible.sync="dialogChangeHeadImgVisible">
      <el-upload
        drag
        ref="uploadheadimg"
        :action="this.GLOBAL.baseURL + '/changeheadimg/'"
        :multiple="false"
        list-type="picture"
        :auto-upload="false"
        :data="{'sessionid': this.$cookies.get('sessionid')}"
        :limit="1">
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip" slot="tip">只能上传jpg/png文件</div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogChangeHeadImgVisible = false">取 消</el-button>
        <el-button type="primary" @click="$refs.uploadheadimg.submit();dialogChangeHeadImgVisible = false">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
      is_login: false,
      username: null,
      password: null,
      name: null,
      dialogChangeHeadImgVisible: false,
      headImgUrl: this.GLOBAL.baseURL + '/media/files/logo.jpg',
      sweet: 999999
    }
  },
  mounted () {
    var that = this
    // Enter事件 --> 登录函数
    document.onkeydown = function (e) {
      var key = window.event.keyCode
      if (key === 13) {
        that.login()
      }
    }
    var data = {
      'sessionid': that.$cookies.get('sessionid')
    }
    // 发送请求检查登录状态
    that.$http.post(that.GLOBAL.baseURL + '/login_status/', data).then(function (res) {
      if (res.status === 200) {
        that.$data.is_login = res.data.state
        if (res.data.state) {
          that.$data.name = res.data.fullname
        }
      }
    }, function (res) {
      console.error(res)
    })
    that.getHeadImgUrl()
  },
  methods: {
    login: function () {
      var that = this
      var data = {
        'username': that.$data.username,
        'password': that.$data.password
      }
      // var formdata = new FormData()
      // formdata.append('username', that.$data.username)
      // formdata.append('username', that.$data.password)
      that.$http.post(that.GLOBAL.baseURL + '/login/', data).then(function (res) {
        if (res.status === 200) {
          if (res.data.msg === 'success') {
            // 登录成功
            that.$cookies.set('sessionid', res.data.sessionid)
            that.$data.name = res.data.fullname
            that.$data.is_login = true
            that.$message({
              type: 'success',
              message: '登录成功'
            })
          } else if (res.data.msg === 'no option') {
            that.$message('没有进行操作')
          } else if (res.data.msg === 'PasswordFailed') {
            that.$message('密码错误')
          } else if (res.data.msg === 'NotExistThisUser') {
            that.$message('不存在该用户')
          }
        }
      }, function (res) {
        console.error(res)
      })
    },
    quitLogin: function () {
      this.$cookies.remove('sessionid')
      location.reload()
    },
    getHeadImgUrl: function () {
      var that = this
      that.$http.get(this.GLOBAL.baseURL + '/getmetainfo/?sessionid=' + that.$cookies.get('sessionid')).then(function (res) {
        if (res.data.msg === 'success') {
          that.$data.headImgUrl = res.data.url
          that.$data.sweet = res.data.sweet
        }
      }, function (err) {
        console.log(err)
      })
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#login_app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  display: flex;
  justify-content: center;
}
#login_box {
  height: 30rem;
  width: 20rem;
  background-color: cadetblue;
  border-radius: 0.8rem;
  display: flex;
  flex-flow: column wrap;
  align-items: center;
  margin-top: 7rem;
}
#title {
  margin-top: 15%;
  color: brown;
  font-size: 2rem;
}
#menu {
  border-bottom: none;
  position: relative;
  /* display: flex;
  align-items: center; */
}

.inputUserName {
  margin-top: 15%;
  width: 15rem;
}
.inputPassWord {
  margin-top: 2rem;
  width: 15rem;
}
.btn {
  margin-top: 3rem;
}
body {
  display: block;
  margin: 0px;
  background: url("assets/background.jpg");
  background-repeat: repeat;
  background-origin: content-box;
  background-position: center center;
  background-attachment: fixed;
}
#Cabecera {
  height: 2.5em;
  width: 2.5em;
  border-radius: 50%;
  position: absolute;
  right: 1rem;
  top: 0.5rem;
}
#fullname {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 3rem;
  width: auto;
  padding-left: 0.5rem;
  padding-right: 0.5rem;
  background-color: skyblue;
  border: 3px solid #00d5ffbb;
  border-radius: 1.5rem;
}
#fullname div {
  display: flex;
}
.elPopover {
  display: flex;
  flex-flow: column wrap;
  align-items: center;
}
.InPopoverContext {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}

/* 心跳样式 */
.heart {
	animation: heartbeat 1s infinite;
	-webkit-animation: heartbeat 1s infinite;
	/* Safari 和 Chrome */
  width: 5rem;
	height: 5rem;
	background: #F00;
	filter: drop-shadow(0px 0px 20px rgb(255,20,20));
	transform: rotate(45deg);
  display: flex;
  justify-content: center;
  margin-top: 0.5rem ;
  margin-bottom: 0.5rem ;
  /* align-items: center; */
}

.heart:before, .heart:after {
	content: "";
	position: absolute;
	width: 5.03rem;
	height: 5.03rem;
	background: #f00;
	border-radius: 100px;
  z-index: -1;
}

.heart:before {
	left: -2.5rem;
}

.heart:after {
	top: -2.5rem;
}

@keyframes heartbeat {

	0% {
		transform: rotate(45deg) scale(0.8,0.8);
		opacity: 1;
	}

	25% {
		transform: rotate(45deg) scale(1,1);
		opacity: 0.8;
	}

	100% {
		transform:rotate(45deg) scale(0.8,0.8);
		opacity: 1;
	}
}

.heart div {
  transform: rotate(-45deg);
  height: auto;
  width: auto;
  color: white;
  text-align: center;
  font-size: 1.2rem;
}

</style>
