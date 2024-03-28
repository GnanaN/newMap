//导入二次封装的axios
import request from '@/utils/request'

// 枚举接口
enum API{
  LOGIN_URL = '/login',
  REGISTER_URL = '/register',
  LOGOUT_URL = '/logout'
}
//登录接口
export const reqLogin = (data:any)=> request.post<any, any>(API.LOGIN_URL,data)
//注册接口
export const reqRegister = (data:any)=> request.post<any, any>(API.REGISTER_URL,data)
//退出登录接口
export const reqLogout = ()=> request.post<any, any>(API.LOGOUT_URL)
