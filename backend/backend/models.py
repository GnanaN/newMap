from django.db import models
import uuid

class upLoadFile(models.Model):

  # name = models.CharField(max_length=255, default=generate_unique_name)  # 文件名
  file_path = models.FileField(upload_to='uploads/')  # 文件路径
  # size = models.IntegerField()  # 文件大小
class AnomalyData(models.Model):
  # upload_to 可以是一个字符串，也可以是一个函数。如果它是一个字符串，
  # 那么这个字符串会被添加到你的 MEDIA_ROOT 设置的路径后面，来形成文件的完整路径。
  # 例如，如果你的 MEDIA_ROOT 是 /var/www/mywebsite/media/，并且 upload_to 是 'uploads/intensity/'，
  # 那么上传的文件会被保存到 /var/www/mywebsite/media/uploads/intensity/ 目录。
  intensity_file = models.FileField(upload_to='submit/intensity/')
  impact_file = models.FileField(upload_to='submit/impact/')
  attribute_file = models.FileField(upload_to='submit/attribute/')
  name = models.CharField(max_length=200)
  type = models.CharField(max_length=200)
  date = models.DateField()

