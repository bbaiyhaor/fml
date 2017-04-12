#encoding=utf-8
from __future__ import unicode_literals
from django.db import models

# Create your models here.
# 用来保存上传图片相关信息的模型
class Profile(models.Model):
    name = models.CharField(max_length = 50)
    # upload_to 表示图像保存路径
    picture = models.ImageField(upload_to = 'face')

    class Meta:
        db_table = "profile"

    def __str__(self):
        return self.name