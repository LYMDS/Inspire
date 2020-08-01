import Vue from 'vue'
import Router from 'vue-router'

import HelloWorld from '@/components/HelloWorld'
import index from '@/components/page/index'
import commit from '@/components/page/commit'
import sendbymyself from '@/components/page/sendbymyself'
import approved from '@/components/page/approved'
import approving from '@/components/page/approving'
import editmission from '@/components/page/editmission'
import publicgift from '@/components/page/publicgift'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(Router)
Vue.use(ElementUI)

const originalPush = Router.prototype.push
Router.prototype.push = function push (location) {
  return originalPush.call(this, location).catch(err => err)
}

export default new Router({
  routes: [
    {
      path: '/HelloWorld',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/',
      name: 'index',
      component: index
    },
    {
      path: '/commit',
      name: 'commit',
      component: commit
    },
    {
      path: '/sendbymyself',
      name: 'sendbymyself',
      component: sendbymyself
    },
    {
      path: '/approved',
      name: 'approved',
      component: approved
    },
    {
      path: '/approving',
      name: 'approving',
      component: approving
    },
    {
      path: '/editmission',
      name: 'editmission',
      component: editmission
    },
    {
      path: '/publicgift',
      name: 'publicgift',
      component: publicgift
    }
  ]
})
