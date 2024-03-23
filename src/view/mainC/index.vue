<template>
  <div class="mainBox" >
    <el-button size="small" style="margin:0px; border-color: aliceblue;" icon="CloseBold" @click="changeScene"></el-button>
    <div class="mapOuterBox" >
      <mapBox ref="mapBox1" class="leftMap" @map-moved="handelMapMoved2"></mapBox>
      <mapBoxMid ref="mapBox2" class="midMap" @map-moved="handelMapMoved1"></mapBoxMid>
    <div class="rightMap">文字展示</div>
    </div>
  </div>
</template>

<script setup lang="ts">
// vue3中的defineEmits方法
//导入组件
import {ref, onMounted} from 'vue'
// const pscene:any = inject('pscene')
import mapBox from './mapBox/index.vue'
import mapBoxMid from './mapBoxMid/index.vue'
// 子传父
const emit = defineEmits(['changemainScene'])
const changeScene = ()=>{
  // console.log( pscene.value)
  emit('changemainScene', 0)
}
const mapBox1 = ref(null)
const mapBox2 = ref(null)

//重置第二个子组件的center和zoom
const handelMapMoved2 = (e:any)=>{
  if(mapBox2.value){
    console.log(mapBox2.value.setMapView(e.center, e.zoom))
  }
}
const handelMapMoved1 = (e)=>{
  if(mapBox1.value){
    console.log(mapBox1.value.setMapView(e.center, e.zoom))
  }

}
onMounted(()=>{
  return mapBox1.value, mapBox2.value

})
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