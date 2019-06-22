from django.db import models

# Create your models here.

# 用户
class WebUser(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
        ('unknown', '保密'),
    )


    username = models.CharField(max_length=20, verbose_name='昵称')
    headPortrait = models.ImageField(upload_to='media/blog/headPortrait/',default='media/blog/headPortrait/icon.png',verbose_name='头像')
    password = models.CharField(max_length=128, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱',unique=True)
    sex = models.CharField(max_length=10,choices=gender,default='unknown')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

# 邮件确认码
class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('WebUser',on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ":   " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"

# 用户设置
class UserSetting(models.Model):
    user = models.ForeignKey('WebUser',on_delete=models.CASCADE,related_name='user_setting',verbose_name='用户')
    live2d = models.BooleanField(default=False,verbose_name='是否开启看板娘')