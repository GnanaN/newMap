<template>
  <div id="mapid1" style="height: 100%"></div>
</template>

<script setup lang="ts">
import {ref, inject, onUnmounted, watch, nextTick, onMounted} from 'vue'
import L from 'leaflet'
let pscene: any = inject('pscene')
import 'leaflet.chinatmsproviders'

let map = ref<any>(null);
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
//初始化地图
const mapValue = {
    crs: L.CRS.EPSG3857,
    center: [32.0603, 118.7969],
    zoom: 12,
    maxZoom: 18,
    minZoom: 5,
    layers: [normalMap],
    zoomControl: true
  }
const initMap = () => {
    map.value = L.map('mapid1', mapValue)

  // Add control layers and zoom control to the map

  L.control.layers(baseLayers, null).addTo(map.value)
  return map.value
}

//定义setMapView方法
const setMapView = (center: L.LatLngExpression, zoom: number) => {
  if (map.value) {
    map.value.setView(center, zoom)
  }
}
//暴露给父组件的方法
defineExpose({ setMapView })

//自定义事件
const emit = defineEmits(['map-moved'])
onMounted(() => {
  const mapInstance = initMap()
  //等初始化完成后，强制地图重新计算大小和位置
  nextTick(() => {
    // 强制地图重新计算大小和位置
    if (mapInstance){
      mapInstance.invalidateSize();
    }
  });

  mapInstance.on('zoomend dragend', () => {
    emit('map-moved', { center: mapInstance.getCenter(), zoom: mapInstance.getZoom() })
  })
})


onUnmounted(() => {
  if (map.value) {
    map.value.remove();
    map.value = null;
  }
})
</script>

<style scoped>
#mapid1 {
  height: 100%;
}
</style>
