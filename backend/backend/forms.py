from django import forms


class SubmitForm(forms.Form):
  name = forms.CharField(label='异常名称')
  type = forms.ChoiceField(label='异常类型', choices=[
    ('fire', '火灾'),
    ('earthquake', '地震'),
    ('algae_bloom', '水华'),
    ('landslide', '滑坡'),
    ('other', '其他'),
  ])
  date = forms.DateField(label='发生时间')
  density_file = forms.FileField(label='异常强度数据')
  impact_file = forms.FileField(label='异常影响数据')
  attribute_file = forms.FileField(label='异常属性数据')


# 上传文件的表单
class UploadFileForm(forms.Form):
  file = forms.FileField(label='文件')
