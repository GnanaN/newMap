import { createRouter, createWebHashHistory } from "vue-router"; //引入createRouter和createWebHashHistory方法
//创建路由实例
const router = createRouter({
  history: createWebHashHistory(),
  //routes对象，其中保存了路由信息
  routes: [
    {
      path: '/login',
      component: () => import('@/view/login/index.vue'),
      name: 'login',
      meta: {
        title: '登录',
        hidden: true,
        icon: 'el-icon-s-home'
      }
    },
    {
      path: '/',
      name: 'layout',
      component: () => import('@/view/layout/index.vue'),
      meta: {
        title: '', //菜单需要的标题
        hidden: false,
        icon: ''
      }
    }
  ]
  //滚动行为，只有在history模式下才有用
  // scrollBehavior(){
  //   return{
  //     left:0,
  //     top:0
  //   }
  // }
})
export default router