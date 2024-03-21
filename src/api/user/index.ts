//导入二次封装的axios
import request from '@/utils/request'

// 枚举接口
enum API{
  LOGIN_URL = '/login'
}
//登录接口
export const reqLogin = (data:any)=> request.post<any, any>(API.LOGIN_URL,data)