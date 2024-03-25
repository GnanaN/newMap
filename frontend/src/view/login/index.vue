<template>
  <div class="login_box">
    <el-row>
      <el-col :span="12" :xs="24">
        <el-form class="login_form" :model="LoginForm" :rules="rules" ref="loginFormRef">
          <h2>地表异常预警平台</h2>
          <el-form-item prop="username">
            <el-input prefix-icon="User" v-model="LoginForm.username"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input type="password" prefix-icon="Lock" v-model="LoginForm.password"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" class="login_but" @click="login">登录</el-button>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="12" :xs="0"></el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { userStore } from '@/store/modules/user'
import {useRouter, useRoute} from 'vue-router'
import { ElNotification } from 'element-plus';
//新建一个loginForm用于收集表单数据
let LoginForm = ref({
  username: '',
  password: ''
})
//获取用户仓库
let ustore = userStore()
//获取路由器
let $router = useRouter()
let $route = useRoute()
//获取表单组件
let loginFormRef = ref()
const login = async()=>{
  await loginFormRef.value.validate()
  //登录逻辑
  //首先，发起请求，将用户名和密码发送给后端
  //然后，后端返回一个token，将token存储在本地
  //最后，跳转到首页
  try{
    await ustore.userLogin(LoginForm.value)
    //如果有redirect参数，就跳转到redirect，否则跳转到首页
    let redirect: any = $route.query.redirect
    $router.push({ path: redirect || '/' })
    // 提示登录成功
    ElNotification({
      title: `欢迎回来${ustore.username}`,
      message: '欢迎回来',
      type: 'success'
    });
  } catch(error){

    // 提示登录失败
    ElNotification({
      type: 'error',
      message: (error as Error).message,
    });
  }
}

const validatorUsername = (rule: any , value:string, callback:any)=>{
  if(value== undefined){
    callback(new Error('用户名不能为空'))
  }
  if(value.length>=5 && value.length<=20){
    callback()
  }else{
    callback(new Error('用户名必须是5-20位的字符串'))
  }
}

const validatorPassword = (rule:any , value:string, callback:any)=>{
  if(value== undefined){
    callback(new Error('密码不能为空'))
  }
  if(value.length > 5){
    callback()
  }else{
    callback(new Error('密码长度必须大于5位'))
  }
}
//定义表达验证需要配置的对象
const rules = {
  username: [
    //validatorUsername在上面定义
   {trigger:'blur', validator: validatorUsername}
  ],
  password: [
    {trigger:'blur', validator:validatorPassword}
  ]
}
</script>

<style lang="scss" scoped>
.login_box {
  width: 100%;
  height: 100%;
  background-image: url('../../assets/login/bg.gif');
  background-size: cover;
  .login_form {
    position: relative;
    padding: 40px;
    width: 60%;
    top: 30vh;
    .login_but{
      width: 100%;
    }
  }
}
</style>
