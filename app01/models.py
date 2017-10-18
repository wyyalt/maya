from django.db import models

class UserInfo(models.Model):
    username = models.CharField(max_length=32,verbose_name="用户名")
    password = models.CharField(max_length=128,verbose_name="密码")

class UserGroup(models.Model):
    title = models.CharField(max_length=32,verbose_name="用户组")