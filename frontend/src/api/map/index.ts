//导入二次封装的axios
import request from '@/utils/request'

// 枚举接口
enum API {
  SUBMIT_FILE = '/submit',
  UPLOAD_FILE = '/upload'
}

//上传文件接口
//上传文件接口
//上传文件接口
export const reqUploadFile = (upLoadData: any) => {
  let formData = new FormData();
  formData.append('file', upLoadData.file);
  return request.post(API.UPLOAD_FILE, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
}
//提交文件接口
export const reqSubmitData = (data: any) => {
  return request.post<any, any>(API.SUBMIT_FILE, data, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}