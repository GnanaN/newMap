import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
//@ts-ignore忽略当前文件ts类型的检测否则有红色提示(打包会失败)
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
//导入svg图标
import 'virtual:svg-icons-register'
import gloablComponent from './components/index'
//导入路由文件
import router from './router'
//导入mock文件
// import configureMockServer from './mock/user.ts';
// configureMockServer()
//导入仓库
import pinia from './store'
//引入leaflet文件
import 'leaflet/dist/leaflet.css'

//创建app实例
const app = createApp(App)
app.use(ElementPlus, { locale: zhCn })
app.use(gloablComponent)
app.use(router)
app.use(pinia)
app.mount('#app')

