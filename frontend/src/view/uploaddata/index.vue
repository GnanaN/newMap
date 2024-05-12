<template>
  <el-card v-if="scene === 0" class="dataShow" >
    <el-button type="primary" size="default" icon="Plus" style="margin-bottom:10px" @click="addData">添加数据</el-button>

    <h3>数据列表</h3>
    <el-table stripe :data="dataShowVar">
      <el-table-column label="序号" type="index" align="center" width="90px"></el-table-column>
        <el-table-column prop="name" label="异常名称" width="180" ></el-table-column>
        <el-table-column prop="type" label="异常类型" width="180" ></el-table-column>
        <el-table-column prop="date" label="发生时间" ></el-table-column>
        <el-table-column prop="operator" label="操作">
          <template #="{ row }">
            <el-button
              size="small"
              icon="Monitor"
              @click="generate(row.id)"
            >综合</el-button>
            <el-popconfirm
              :title="`确定要删除${row.attrName}属性吗？`"
              width="250px"
              @confirm="deleteData(row.id)"
            >
              <template #reference>
                <el-button
                  size="small"
                  icon="Delete"
                >删除</el-button>
              </template>
            </el-popconfirm>
            <el-button size="small" icon="View"  @click="scene=2">展示</el-button>
          </template>
        </el-table-column>
    </el-table>
  </el-card>
  <el-card v-if="scene === 1" class="dataLoad">
    <el-form label-width="100px">
      <el-form-item label="异常名称">
        <el-input v-model="dataUpLoadVar.name"></el-input>
      </el-form-item>
      <el-form-item label="异常类型" >
        <el-select v-model="dataUpLoadVar.type">
          <el-option label="火灾" value="火灾"></el-option>
          <el-option label="地震" value="地震"></el-option>
          <el-option label="水华" value="水花"></el-option>
          <el-option label="滑坡" value="滑坡"></el-option>
          <el-option label="其他" value="other"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="发生时间" >
        <el-input type="date"  v-model="dataUpLoadVar.date"></el-input>
      </el-form-item>
      <el-form-item label="异常强度数据" >
        <div class="uploadDiv">
          <upload ref="loadIntensity" ></upload>
        </div>
      </el-form-item>
      <el-form-item label="异常影响数据" >
        <div class="uploadDiv">
          <upload ref="loadInfluence" ></upload>
        </div>
      </el-form-item>
      <el-form-item label="异常属性数据" >
        <div class="uploadDiv">
          <upload ref="loadProperty" ></upload>
        </div>
      </el-form-item>
    </el-form>
    <div class="btnPosition">
      <el-button type="primary" size="default" @click="cancel">取消</el-button>
      <el-button type="primary" size="default" @click="submitData">提交</el-button>
    </div>
  </el-card>
  <!-- ref="mainCRef" 控制子组件 -->
  <mainC v-if="scene === 2"  @changemainScene="changeSceneTo" ></mainC>
</template>

<script setup lang="ts">
import {ref, provide, watch, onBeforeMount, toRaw} from 'vue'
import {reqSubmitData, reqGetData, reqDeleteData,reqGenerateData} from '@/api/map/index'
import upload from './upload/index.vue'
import mainC from '@/view/mainC/index.vue'
import { ElMessage } from 'element-plus';
let scene = ref(0)
// 父传给子的属性
// let intensityFileList:Array<any> =[];
// let impactFileList:Array<any> = [];
// let attributeFileList:Array<any> = [];
provide('pscene', scene)
//数据上传页面所需变量
let dataUpLoadVar = ref<any>({
  name:'',
  type:'',
  date:'',
})
let dataShowVar = ref<any[]>([{
  name:'',
  type:'',
  date:'',
  intensity_file:'',
  impact_file:'',
  attribute_file:''

}])
// 获取子组件的实例
const loadIntensity = ref()
const loadInfluence = ref()
const loadProperty = ref()
// let mainCRef = ref()
const addData = ()=>{
  scene.value = 1
  console.log('添加数据')
  //导入本地数据

}
const submitData = () => {
  console.log('提交数据')
  const formData = new FormData()
  formData.append('name', dataUpLoadVar.value.name)
  formData.append('type', dataUpLoadVar.value.type)
  formData.append('date', dataUpLoadVar.value.date)
  // console.log(loadIntensity.value.fileList[0].url)
  // console.log(loadInfluence.value.fileList[0].url)
  // console.log(loadProperty.value.fileList[0].url)
  formData.append('intensity_file',loadIntensity.value.fileList[0].url)
  formData.append('impact_file', loadInfluence.value.fileList[0].url)
  formData.append('attribute_file', loadProperty.value.fileList[0].url)
  formData.append('intensity_file_id',loadIntensity.value.fileList[0].id)
  formData.append('impact_file_id', loadInfluence.value.fileList[0].id)
  formData.append('attribute_file_id', loadProperty.value.fileList[0].id)

  // 打印 FormData 对象的内容
  for (let [key, value] of formData.entries()) {
    console.log(key, value)
  }

  // 提交数据
  reqSubmitData(formData).then(res => {
    console.log(res)
    if (res.code === 200) {
      console.log('提交成功')
    } else {
      console.log('提交失败')
      ElMessage.error('提交失败')
    }
  })
  // 清空数据
  dataUpLoadVar = Object.assign(dataUpLoadVar.value, {
    name: '',
    type: '',
    date: '',
    // ...
  })

  //切换场景
  scene.value = 0

}

const cancel = ()=>{
  console.log('取消')
  // 清空数据
  dataUpLoadVar =  Object.assign(dataUpLoadVar.value,{
    name:'',
    type:'',
    date:'',
    intensity:'',
    influence:'',
    property:''
  })
  //切换场景
  scene.value = 0
}
const changeSceneTo = (num: number)=>{
  scene.value = num
}
// 获取数据
const getData = async()=>{
  const res = await reqGetData()
  if (res.code === 200){
    dataShowVar.value = res.data
  }
  else{
    console.log('获取数据失败')
  }
}
// 场景切换为0时获取数据，更新表格
watch(scene, (newVal)=>{
  if (newVal === 0){
    getData()
  }
})
// 挂载之前获取数据
onBeforeMount(()=>{
  getData()
})
//删除数据的函数
const deleteData = async(row : any) => {
  console.log('row',row)
  //删除输入的数据要符合后端要求的格式
  const body_json = {'id': row}
  const res = await reqDeleteData(body_json)
  if (res.code === 200){
    console.log('删除成功')
    getData()
  }
  else{
    console.log('删除失败')
  }
}
//综合按钮对应的函数
const generate = async(row : any) => {
  console.log('row',row)
  //删除输入的数据要符合后端要求的格式
  const body_json = {'id': row}
  const res = await reqGenerateData(body_json)
  if (res.code === 200){
    console.log('综合成功')

    scene.value = 2
  }
  else{
    console.log('综合失败')
  }
}


</script>

<style lang="scss" scoped>
.dataLoad{
  margin:10px;
  padding:10px;
  width:40%;
  height:60%;
  overflow:auto;
}
.dataShow{
  margin:10px;
  padding:10px;
  width:100%;
  height:95%;
  overflow:auto;

}
.uploadDiv {
  width: 100%;
  height: 50px;
  border: 1px solid rgb(192, 190, 190);
  border-radius: 5px;
}
.btnPosition{
  display:flex;
  justify-content: flex-end;
}
</style>
