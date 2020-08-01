// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import VueCookies from 'vue-cookies'

// 引入全局变量
import globalVariables from '@/api/global_variables.js'
// 引入全局函数
import globalFunctions from '@/api/global_function'
// 引入VueResource
import VueResource from 'vue-resource'

Vue.use(VueCookies)
Vue.use(VueResource)
Vue.http.interceptors.push(function (request, next) { // 拦截器
  // 跨域携带cookie
  request.credentials = true
  console.log('设置跨域')
  next()
})

// 定义全局变量
Vue.prototype.GLOBAL = globalVariables
// 使用全局函数
Vue.use(globalFunctions)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
