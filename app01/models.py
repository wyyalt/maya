from django.db import models

class UserInfo(models.Model):
    username = models.CharField(max_length=32,verbose_name="用户名")
    password = models.CharField(max_length=128,verbose_name="密码")
    user_city = models.ForeignKey("UserCity",verbose_name="城市")
    user_group = models.ManyToManyField("UserGroup",verbose_name="用户组")

    def __str__(self):
        return self.username


    def user_pass(self):
        return "%s-%s"%(self.username,self.password)

class UserGroup(models.Model):
    title = models.CharField(max_length=32,verbose_name="用户组")

    def __str__(self):
        return self.title

class UserCity(models.Model):
    title = models.CharField(max_length=32,verbose_name="城市")

    def __str__(self):
        return self.title