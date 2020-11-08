# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

# 在企业开发中
  # model -> sql
  # sql -> model
    # django也提供了很好的支持
    # python manage.py inspectdb
      # 可以直接根据表生成模型
      # 元信息中包含一个属性 managed=False表示不是通过django的模型迁移生成的 是自己管理的
 # 如果自己的模型不想被迁移系统管理, 也可以使用 managed=False进行声明
# 先删除app中models.py文件 在用命令重定向输出python manage.py inspectdb > App/models.py
class Book(models.Model):
    b_name = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book'




class User(models.Model):
    u_name = models.CharField(max_length=16)
    # upload_to 相对路径  相对于的是MEDIA_ROOT 媒体根目录
    # 需要在settings中配置静态资源地址 MEDIA_ROOT = os.path.join(BASE_DIR, 'static/upload')
    # upload_to='%Y/%m/%d/icons' 按照年月日一层一层路径保存  能避免Linux的bug(一个文件存放的个数超过65535个就打不开的问题)
    u_icon = models.ImageField(upload_to='%Y/%m/%d/icons')

