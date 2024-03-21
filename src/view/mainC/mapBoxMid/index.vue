<template>
  <div id="mapid1" style="height: 100%"></div>
</template>

<script setup lang="ts">
import {ref, inject, onUnmounted,  watch, nextTick} from 'vue'
import L from 'leaflet'
let pscene: any = inject('pscene')
import 'leaflet.chinatmsproviders'

let map = ref<any>(null);
//初始化地图
const initMap = () => {
  // const mapKey = 'gc0313a16b7141d25ae197a72e2ce004bn'
  // Define different tile layers for map display
  // TianDiTu normal and satellite map layers

  // Geoq normal layers
  const normalm3 = L.tileLayer.chinaProvider(
    'Geoq.Normal.PurplishBlue',
    {}
  )
  // Google map layers
  const normalMap = L.tileLayer.chinaProvider('Google.Normal.Map', {})
  const satelliteMap = L.tileLayer.chinaProvider(
    'Google.Satellite.Map',
    {}
  )
  // 高德地图
  const Gaode = L.tileLayer.chinaProvider('GaoDe.Normal.Map', {})
  const Gaodimage = L.tileLayer.chinaProvider('GaoDe.Satellite.Map', { })


  // Create base layers with different tile layers
  const baseLayers = {
    智图午夜蓝: normalm3,
    谷歌地图: normalMap,
    谷歌影像: satelliteMap,
    高德地图: Gaode,
    高德影像: Gaodimage,
  }

  // Initialize the map

    map.value = L.map('mapid1', {
    crs: L.CRS.EPSG3857,
    center: [32.0603, 118.7969],
    zoom: 12,
    maxZoom: 18,
    minZoom: 5,
    layers: [normalMap],
    //缩放控制插件
    zoomControl: true
  })

  // Add control layers and zoom control to the map

  L.control.layers(baseLayers, null).addTo(map.value)
  return map.value
}

watch(() => pscene.value, (newValue, oldValue) => {
  if (newValue == 2) {
    console.log('地图组件')
    initMap()
  }
  if (oldValue == 2 && newValue != 2) {
    console.log('地图组件隐藏')
    if (map.value) {
      map.value.remove();
      map.value = null;
    }
  }
  nextTick(() => {
    // 强制地图重新计算大小和位置
    if (map.value){
      map.value.invalidateSize();
    }
  });
})


onUnmounted(() => {
  if (map.value) {
    map.value = null;
  }
})
</script>

<style scoped>
#mapid1 {
  height: 100%;
}
</style>
