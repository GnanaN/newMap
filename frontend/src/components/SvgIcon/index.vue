<template>
  <svg :style="{ width, height }">
    <use :xlink:href="prefix + icon_name" :fill="icon_color"></use>
  </svg>
</template>

<script setup lang="ts">
//接受父组件传过来的参数
defineProps({
  prefix: {
    type: String,
    default: '#icon-',
  },
  //提供使用的图标的名字
  icon_name: String,
  //父组件传递的颜色
  icon_color: {
    type: String,
    default: '',
  },
  //接受父组件传递来的图标的宽和高
  width: {
    type: String,
    default: '16px',
  },
  height: {
    type: String,
    default: '16px',
  },
})
</script>

<style scoped></style>
