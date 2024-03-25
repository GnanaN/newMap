<template>
  <el-card v-if="scene === 0" class="dataShow">
    <el-button type="primary" size="default" icon="Plus" style="margin-bottom:10px" @click="addData">添加数据</el-button>
    <el-button type="primary" size="default" icon="Plus" style="margin-bottom:10px" @click="scene=2">抽屉</el-button>
    <h3>数据列表</h3>
    <el-table stripe>
    <el-table-column prop="name" label="异常名称" width="180"></el-table-column>
    <el-table-column prop="type" label="异常类型" width="180"></el-table-column>
    <el-table-column prop="date" label="发生时间"></el-table-column>
    <el-table-column prop="operator" label="操作">
      <el-button icon="Monitor">综合</el-button>
      <el-button icon="Delete">删除</el-button>
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
          <el-option label="火灾" value="fire"></el-option>
          <el-option label="地震" value="earthquake"></el-option>
          <el-option label="水华" value="algae_bloom"></el-option>
          <el-option label="滑坡" value="landslide"></el-option>
          <el-option label="其他" value="other"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="发生时间" >
        <el-input type="date"  v-model="dataUpLoadVar.date"></el-input>
      </el-form-item>
      <el-form-item label="异常强度数据" >
        <div class="uploadDiv">
          <upload ref="loadIntensity"></upload>
        </div>
      </el-form-item>
      <el-form-item label="异常影响数据" >
        <div class="uploadDiv">
          <upload ref="loadInfluence"></upload>
        </div>
      </el-form-item>
      <el-form-item label="异常属性数据" >
        <div class="uploadDiv">
          <upload ref="loadProperty"></upload>
        </div>
      </el-form-item>
    </el-form>
    <div class="btnPosition">
      <el-button type="primary" size="default" @click="cancel">取消</el-button>
      <el-button type="primary" size="default" @click="submitData">提交</el-button>
    </div>
  </el-card>
  <!-- ref="mainCRef" 控制子组件 -->
  <mainC v-if="scene === 2"  @changemainScene="changeSceneTo"></mainC>
</template>

<script setup lang="ts">
import {ref, provide} from 'vue'
import upload from './upload/index.vue'
import mainC from '@/view/mainC/index.vue'
let scene = ref(0)
provide('pscene', scene)
//数据上传页面所需变量
let dataUpLoadVar = ref<any>({
  name:'',
  type:'',
  date:'',
  intensity:'',
  influence:'',
  property:''
})
// 获取子组件的实例
let loadIntensity = ref()
let mainCRef = ref()
const addData = ()=>{
  scene.value = 1
  console.log('添加数据')
  //导入本地数据

}
const submitData = ()=>{
  console.log('提交数据')
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
