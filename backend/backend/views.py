import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render
import zipfile
from backend.genecoded import main as gene_main
import logging
from osgeo import gdal
logger = logging.getLogger(__name__)


# 注册
@csrf_exempt
def register(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    # 验证用户名长度
    if len(username) < 5 or len(username) > 20:
      return JsonResponse({'status': 'error', 'code': 400, 'message': 'Username must be at least 5 to 20 characters'}, status=400)

    # 验证密码长度和格式
    if len(password) < 6 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
      return JsonResponse({'status': 'error', 'code': 400, 'message': 'Password must be at least 6 characters and contain at least one digit and one letter'}, status=400)

    user = User.objects.create_user(username, password=password)
    return JsonResponse({'status': 'success', 'code': 201}, status=201)

# 登录
@csrf_exempt
def login_view(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      # 返回json数据
      return JsonResponse({
        'status': 'success',
        'code': 200,
        'data': {
          'token': request.session.session_key,
          'username': username,
          'avatar': ''
          # 其他你想返回的数据
        }
      }, status=200)
    else:
      return JsonResponse({'status': 'error', 'code': 401, 'message': 'Invalid credentials'}, status=401)
  else:
    return JsonResponse({'status': 'error', 'code': 400, 'message': 'Invalid request method'}, status=400)

# 登出
def logout_view(request):
  request.session.flush()
  return JsonResponse({'status': 'success', 'code': 200}, status=200)


from django.core.files.storage import FileSystemStorage
from .models import AnomalyData, upLoadFile

# 上传文件
@csrf_exempt
def upload_file(request):
  if request.method == 'POST':
    uploaded_file = request.FILES['file']
    fs = FileSystemStorage('uploads/')
    name = fs.save(uploaded_file.name, uploaded_file)
    file_url = fs.url(name)

    # 保存文件路径到数据库
    upLoad_data = upLoadFile(file_path=file_url)
    upLoad_data.save()

    return JsonResponse({
      'status': 'success',
      'code': 200,
      'data': {
        'id': upLoad_data.id,
        'file_url': file_url,
        'name': name
      }
    })

  return JsonResponse({
    'code': 400,
    'error': 'Invalid method',
    'status': 'failed'
  })

# 提交表单
@csrf_exempt
def submit_form(request):
  if request.method == 'POST':
    name = request.POST.get('name')
    type = request.POST.get('type')
    date = request.POST.get('date')
    intensity_file = request.POST.get('intensity_file')
    impact_file = request.POST.get('impact_file')
    attribute_file = request.POST.get('attribute_file')
    intensity_file_id = request.POST.get('intensity_file_id')
    impact_file_id = request.POST.get('impact_file_id')
    attribute_file_id = request.POST.get('attribute_file_id')
    print(name, type, date, intensity_file, impact_file, attribute_file)
    if not all([name, type, date, intensity_file, impact_file, attribute_file]):
      return JsonResponse({'status': 'fail', 'code': 400, 'message': 'Missing required fields'})
    anomaly_data = AnomalyData(name=name, type=type, date=date, intensity_file=intensity_file,
                               impact_file=impact_file, attribute_file=attribute_file,
                               intensity_file_id=intensity_file_id, impact_file_id=impact_file_id, attribute_file_id=attribute_file_id)
    anomaly_data.save()
    return JsonResponse({'status': 'success', 'code': 200})

# 获取数据
@csrf_exempt
def get_data(request):
  if request.method == 'GET':
    data = AnomalyData.objects.all()
    data_list = []
    for item in data:
      data_list.append({
        'id': item.id,
        'name': item.name,
        'type': item.type,
        'date': item.date,
        'intensity_file': item.intensity_file.url,
        'impact_file': item.impact_file.url,
        'attribute_file': item.attribute_file.url
      })
    return JsonResponse({'status': 'success', 'code': 200, 'data': data_list})
  return JsonResponse({'status': 'fail', 'code': 400, 'message': 'Invalid request method'})



# 删除数据，不仅要删除AnomalyData表中的数据，还要删除上传的文件也就是UploadFile表中的数据
@csrf_exempt
def delete_data(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    id = data.get('id')
    if not id:
      return JsonResponse({'status': 'fail', 'code': 400, 'message': 'Missing required fields'})
    file = AnomalyData.objects.filter(id=id).first()
    if file:
      AnomalyData.objects.filter(id=id).delete()
      intensity_file = upLoadFile.objects.filter(id=file.intensity_file_id).first()
      impact_file = upLoadFile.objects.filter(id=file.impact_file_id).first()
      attribute_file = upLoadFile.objects.filter(id=file.attribute_file_id).first()
      if intensity_file:
        file_path = os.path.join(settings.MEDIA_ROOT, str(intensity_file.file_path))
        print(file_path)
        if os.path.exists(file_path):
          os.remove(file_path)
        intensity_file.delete()
      if impact_file:
        file_path = os.path.join(settings.MEDIA_ROOT, str(impact_file.file_path))
        if os.path.exists(file_path):
          os.remove(file_path)
        impact_file.delete()
      if attribute_file:
        file_path = os.path.join(settings.MEDIA_ROOT, str(attribute_file.file_path))
        if os.path.exists(file_path):
          os.remove(file_path)
        attribute_file.delete()
      file.delete()
    response_data = {
      'status': 'success',
      'code': 200,
      'args': data,  # 请求参数
      'headers': dict(request.headers),  # 请求头
      'url': request.build_absolute_uri(),  # 请求的完整 URL
    }
    return JsonResponse(response_data)
  return JsonResponse({'status': 'fail', 'code': 400, 'message': 'Invalid request method'})

# 删除上传的文件
import os
from django.conf import settings
@csrf_exempt
def delete_file(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    print(data)
    id = data.get('id')
    if not id:
      return JsonResponse({'status': 'fail', 'code': 400, 'message': 'Missing required fields'})
    file = upLoadFile.objects.filter(id=id).first()
    if file:
      file_path = os.path.join(settings.MEDIA_ROOT, str(file.file_path))
      if os.path.exists(file_path):
        os.remove(file_path)
      file.delete()
      return JsonResponse({'status': 'success', 'code': 200})
    return JsonResponse({'status': 'fail', 'code': 400, 'message': 'File not found'})
  return JsonResponse({'status': 'fail', 'code': 400, 'message': 'Invalid request method'})

# 综合请求
#
# 接收当前灾害的id，返回当前灾害的综合数据
# 首先要获取所需文件的路径，然后解压，对文件中的数据进行处理，最后返回处理后的数据
# 1、解压强度数据
# 2、将强度的地图上传到geoserver，返回地图的url
# 解压影响数据
# 将影响的地图上传到geoserver，返回地图的url
# 解压属性数据
# 使用这些数据进行分析，得到最终的强度综合后地图、影响综合后地图、将这两张地图上传到geoserver
# 返回这两张地图的url

# 解压文件需要的文件路径
def unzip_file(zip_filepath, dest_path):
    dest_path = dest_path + '\\' + zip_filepath.split('\\')[-1].split('.')[0]
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(dest_path)
    return dest_path




# 综合请求
@csrf_exempt
def gene(request):
  print(request.method)
  if request.method == 'POST':
    data = json.loads(request.body)
    id = data.get('id')
    if not id:
      return JsonResponse({'status': 'fail', 'code': 400, 'message': 'Missing required fields'})
    file = AnomalyData.objects.filter(id=id).first()
    if file:
      # 解压文件
      intensity_file = intensity_file = upLoadFile.objects.filter(
          id=file.intensity_file_id).first()

      intensity_file_path = os.path.join(settings.MEDIA_ROOT, str(intensity_file.file_path))
      ## 解压文件并返回解压后的文件路径
      intensity_file_path_unzip = unzip_file(
          intensity_file_path, r'E:\web\项目\new_map\datapath')
      # 处理数据
      ## 设置两个result和temp路径，用于存放处理后的数据
      result_path = r'E:\web\项目\new_map\datapath\result'
      temp_path = r'E:\web\项目\new_map\datapath\temp'
      print(intensity_file_path_unzip)
      logger.info('Before calling gene_main.main')
      result = gene_main.main(intensity_file_path_unzip, result_path, temp_path)
      logger.info('After calling gene_main.main')
      print(result)
      # 上传地图到geoserver
      geoserver = 'http://localhost:8100/geoserver'
      workspac = 'unusal'
      store = ['unusual_shpfile', 'unusal_tiffile']
      username = 'admin'
      password = 'geoserver'
      # 原始图像的tif
      org_tif_url = publish_geoserver_layer(result.get('org_tif'), geoserver, workspac, store, username, password)
      # 处理后的tif
      print('okkkkkk')
      res_tif_url = publish_geoserver_layer(result.get(
          'result_tif_path'), geoserver, workspac, store, username, password)
      # 处理后的shp
      res_shp_url = publish_geoserver_layer(result.get(
          'result_shp_path'), geoserver, workspac, store, username, password)
      # 处理后的凸包shp
      hull_tif_url = publish_geoserver_layer(result.get(
          'hull_shp_path'), geoserver, workspac, store, username, password)
      result.setdefault('org_tif_url', org_tif_url)
      result.setdefault('res_tif_url', res_tif_url)
      # 读取到一个shp文件之后,要把它所有的文件都上传到geoserver上 shp文件,shx文件,dbf文件,prj文件
      # result.setdefault('res_shp_url', res_shp_url)
      # result.setdefault('hull_tif_url', hull_tif_url)
      print(result)
      logger.info('Handling request: %s %s', request.method, request.path)
      # 将有效数据存储到数据库中方便后续调用
      return JsonResponse({'status': 'success', 'code': 200, 'data': result})
    return JsonResponse({'status': 'fail', 'code': 400, 'message': 'File not found'})
  return JsonResponse({'status': 'fail', 'code': 400, 'message': 'Invalid request method'})


import requests
import os


# 上传地图到geoserver
def publish_geoserver_layer(file_path, geoserver_url, workspace_name, store_name, username, password):
  # 判断文件类型
  if file_path.endswith('.tif'):
    content_type = "image/tiff"
    url_file_type = "file.geotiff"
    store_name = store_name[1]
  elif file_path.endswith('.zip'):
    content_type = "application/zip"
    url_file_type = "file.shp"
    store_name = store_name[0]
  else:
    print("Unsupported file type")
    return None
  bbox = calculate_bbox(file_path)
  # 构建请求 URL
  url = f"{geoserver_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}/{url_file_type}"

  # 设置请求头
  headers = {
    "Content-type": content_type,
  }

  # 读取地图文件
  with open(file_path, "rb") as file:
    map_data = file.read()

  # 发送请求
  response = requests.put(url, headers=headers, data=map_data, auth=(username, password))

  # 检查响应
  if response.status_code == 201:
    print("地图上传成功")
    # 构建并返回地图的 URL
    map_url = f"{geoserver_url}/{workspace_name}/wms?service=WMS&version=1.1.0&request=GetMap&layers={workspace_name}:{store_name}&styles=&bbox={bbox}&width=768&height=768&srs=EPSG:4326&format=application/openlayers"
    return map_url
  else:
    print(f"地图上传失败，响应代码：{response.status_code}，响应内容：{response.text}")
    return None

# 计算地图文件的地理范围
def calculate_bbox(file_path):
  # 打开地图文件
  dataset = gdal.Open(file_path)

  # 读取地图文件的元数据
  metadata = gdal.Info(dataset, options=["-json"])

  # 提取地图文件的地理范围
  bbox = metadata["wgs84Extent"]["coordinates"][0]

  # 格式化地理范围
  bbox = ",".join([f"{coord[0]} {coord[1]}" for coord in bbox])
  # print(file_path, bbox)
  return bbox


