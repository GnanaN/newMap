//存放用户数据的仓库
import { defineStore } from 'pinia'
import { reqLogin } from '@/api/user'
import { SET_TOKEN, GET_TOKEN, } from '@/utils/token'
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
        return Promise.reject(new Error(res.message))
      }
    }
  }
})

