//存放用户数据的仓库
import { defineStore } from 'pinia'
import { reqLogin, reqRegister, reqLogout } from '@/api/user'
import { SET_TOKEN, GET_TOKEN, REMOVE_TOKEN } from '@/utils/token'
export const userStore = defineStore({
  id: 'user',
  state: () => {
    return {
      token: GET_TOKEN(),
      username: '',
      avatar: ''
    }
  },
  //异步操作
  actions: {
    //登录
    async userLogin(data: any) {
      const res = await reqLogin(data)
      if (res.code === 200) {
        //将用户名、头像存入仓库
        this.username = res.data.username
        this.avatar = res.data.avatar
        //将token存入localStorage
        SET_TOKEN(res.data.token)
      } else {
        //登录失败
        console.log('登录失败', res.message)
        return Promise.reject(new Error(res.message))
      }
    },
    async userRegister(data: any) {
      const res = await reqRegister(data)
      if (res.code === 201) {
        console.log('注册成功', res)
      } else {
        //登录失败
        console.log('注册失败', res.message)
        return Promise.reject(new Error(res.message))
      }
    },
    //退出登录
    async userLogout() {
      const res = await reqLogout()
      if (res.code === 200) {
        //清空仓库
        this.username = ''
        this.avatar = ''
        //清空localStorage
        REMOVE_TOKEN()
      } else {
        console.log('退出失败', res.message)
        return Promise.reject(new Error(res.message))
      }
    }
  }
})

