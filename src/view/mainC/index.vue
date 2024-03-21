<template>
  <div class="mainBox">
    <el-button size="small" style="margin:0px; border-color: aliceblue;" icon="CloseBold" @click="changeScene"></el-button>
    <div class="mapOuterBox">
      <div class="leftMap">
        <mapBox></mapBox>
      </div>
      <div class="midMap">
        <mapBoxMid></mapBoxMid>
      </div>
      <div class="rightMap">
        文字展示
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// vue3中的defineEmits方法
//导入组件
// import { inject } from 'vue'
// const pscene:any = inject('pscene')
import mapBox from './mapBox/index.vue'
import mapBoxMid from './mapBoxMid/index.vue'
// 子传父
const emit = defineEmits(['changemainScene'])
const changeScene = ()=>{
  // console.log( pscene.value)
  emit('changemainScene', 0)
}

</script>

<style scoped>
.mainBox{
  width:100vw;
  height:88vh;
  background-color: #ffffff;
  position:absolute;
  bottom: 0px;
  left: 0px;
  .mapOuterBox{
    display:flex;
    height:100%;
    .leftMap{
      margin:2px;
      flex:1;
    }
    .midMap{
      margin:2px;
      flex:1;
    }
    .rightMap{
      margin:2px;
      flex:1;
      background-color: #5a0707;
  }
}
}
</style>