<template>
  <div class="outer_box">
    <div class="inner_left"></div>
    <div class="inner_right">
      <div class="inner_top"></div>
      <div class="inner_bottom">
        <uploaddata></uploaddata>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import uploaddata from '@/view/uploaddata/index.vue'
</script>

<style lang='scss' scoped>
.outer_box{
  width:100%;
  height:100%;
  display:flex;
  .inner_left{
    background-color: rgb(162, 213, 181);
    flex:1;
  }
  .inner_right{
    flex:5;
    display: flex;
    flex-direction: column;
    .inner_top{
      background-color: #deabab;
      flex:1
    }
    .inner_bottom{
      display: flex;
      justify-content: center;
      padding:10px;
      background-color: #bcdfe8;
      flex:10
    }
  }
}
</style>