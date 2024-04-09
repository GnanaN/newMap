<template>
  <el-upload
    v-model:fileList="fileList"
    accept=".zip"
    class="divBoxofUpload"
    action="http://127.0.0.1:8000/upload"
    multiple
    :show-file-list="true"
    :on-preview="handlePreview"
    :on-remove="handleRemove"
    :before-remove="beforeRemove"
    :limit="1"
    :on-exceed="handleExceed"
    :on-change="handleChange"
    :http-request="uploadData"
    >
    <el-button size="default" type="primary" style="margin-right:10px;">点击上传压缩包</el-button>

  </el-upload>
</template>

<script setup lang="ts">
  import { ref, toRaw } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import{ reqUploadFile, reqDeleteFile } from '@/api/map/index'
  import type { UploadProps } from 'element-plus'

  let fileList = ref<any[]>([])
  let uploadFlag = ref(false)
  let id = ref()
  const handlePreview: UploadProps['onPreview'] = (uploadFile) => {
    console.log(uploadFile)
  }

  const handleExceed: UploadProps['onExceed'] = (files, uploadFiles) => {
    ElMessage.warning(
      `The limit is 1, you selected ${files.length} files this time, add up to ${
        files.length + uploadFiles.length
      } totally`
    )
  }

  const beforeRemove = (uploadFile) => {
    id = toRaw(fileList.value)[0].id
    return ElMessageBox.confirm(
      `确定要取消上传 ${uploadFile.name} ?`
    ).then(
      () => true,
      () => false
    )
  }

  const handleRemove: UploadProps['onRemove'] = () => {
    console.log(id)
    const body_json = {'id': id}
    reqDeleteFile(body_json).then(res => {
    console.log(res)
      if (res.code === 200) {
        ElMessage.success('Delete success')
        fileList.value = []
        uploadFlag.value = false
      } else {
        ElMessage.error('Delete failed')
      }
    })

  }
  const handleChange: UploadProps['onChange'] = (uploadFile, uploadFiles) => {

  }
  const handleSuccess: UploadProps['onSuccess'] = () => {
  }
  const uploadData: UploadProps['httpRequest'] = async(uploadData) => {
    const res = await reqUploadFile(uploadData)
    console.log(res)
    if (res.code === 200) {
      // console.log(res.data.name,res.data.file_url)
      fileList.value = [{id:res.data.id,name:res.data.name , url:res.data.file_url}]
      console.log('fileList',toRaw(fileList.value))
      uploadFlag.value = true
    } else {
      ElMessage.error('Upload failed')
    }
  }

  defineExpose({
        fileList,
        uploadFlag
      })
</script>

<style scoped>
.divBoxofUpload {
  padding-left: 10px;
  display: flex;
  align-items: center;
}
</style>