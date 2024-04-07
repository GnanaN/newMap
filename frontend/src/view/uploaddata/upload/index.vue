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
    :on-success="handleSuccess"
    :http-request="uploadData"
    >
    <el-button size="default" type="primary" style="margin-right:10px;">点击上传压缩包</el-button>

  </el-upload>
</template>

<script setup lang="ts">
  import { ref, toRaw } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import{ reqUploadFile } from '@/api/map/index'
  import type { UploadProps } from 'element-plus'

  let fileList = ref<any[]>([])
  let uploadFlag = ref(false)
  const handleRemove: UploadProps['onRemove'] = (file, uploadFiles) => {
    console.log(file, uploadFiles)
  }

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

  const beforeRemove: UploadProps['beforeRemove'] = (uploadFile, uploadFiles) => {
    return ElMessageBox.confirm(
      `Cancel the transfer of ${uploadFile.name} ?`
    ).then(
      () => true,
      () => false
    )
  }
  const handleChange: UploadProps['onChange'] = (uploadFile, uploadFiles) => {

  }
  const handleSuccess: UploadProps['onSuccess'] = () => {

  }
  const uploadData: UploadProps['httpRequest'] = async(uploadData) => {
    const res = await reqUploadFile(uploadData)
    if (res.code === 200) {
      console.log(res.data.name,res.data.file_url)
      fileList.value = [{name:res.data.name , url:res.data.file_url}]
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