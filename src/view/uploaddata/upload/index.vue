<template>
  <el-upload
    v-model:fileList="fileList"
    accept=".zip"
    class="divBoxofUpload"
    action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
    multiple
    :show-file-list="true"
    :on-preview="handlePreview"
    :on-remove="handleRemove"
    :before-remove="beforeRemove"
    :limit="1"
    :on-exceed="handleExceed"
    :on-change="handleChange"
    >
    <el-button size="default" type="primary" style="margin-right:10px;">点击上传压缩包</el-button>

  </el-upload>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'

  import type { UploadProps, UploadUserFile } from 'element-plus'

  const fileList = ref<UploadUserFile[]>([

  ])

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
    fileList.value = uploadFiles
  }
</script>

<style scoped>
.divBoxofUpload {
  padding-left: 10px;
  display: flex;
  align-items: center;
}
</style>