import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render

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
    print(name, type, date, intensity_file, impact_file, attribute_file)
    if not all([name, type, date, intensity_file, impact_file, attribute_file]):
      return JsonResponse({'status': 'fail', 'code': 400, 'message': 'Missing required fields'})
    anomaly_data = AnomalyData(name=name, type=type, date=date, intensity_file=intensity_file, impact_file=impact_file, attribute_file=attribute_file)
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




@csrf_exempt
def delete_data(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    id = data.get('id')
    if not id:
      return JsonResponse({'status': 'fail', 'code': 400, 'message': 'Missing required fields'})
    AnomalyData.objects.filter(id=id).delete()
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
# @csrf_exempt
