from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
# Create your models here.


# 用户
class WebUser(models.Model):
    gender = {
        ('male','男'),
        ('female','女'),
        ('unknown','保密'),
    }

    username = models.CharField(max_length=20, verbose_name='名称',unique=True)
    headPortrait = models.ImageField(upload_to='media/blog/headPortrait/',default='media/blog/headPortrait/icon.png',verbose_name='头像')
    password = models.CharField(max_length=128, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱',unique=True)
    sex = models.CharField(max_length=32,choices=gender,default='unknown')
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


class UserSetting(models.Model):
    user = models.ForeignKey('WebUser',on_delete=models.CASCADE,related_name='user_setting',verbose_name='用户')
    live2d = models.BooleanField(default=False,verbose_name='是否开启看板娘')

# 分类
class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name='标签名')
    sensitive = models.BooleanField(verbose_name='敏感', default=0)
    hide = models.BooleanField(verbose_name='隐藏', default=0)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 标签
class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='标签名')
    sensitive = models.BooleanField(verbose_name='敏感',default=0)
    hide = models.BooleanField(verbose_name='隐藏',default=0)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name




# 文章
class Article(models.Model):
    title = models.CharField(max_length=20,default=None,verbose_name='标题')
    category = models.ForeignKey('Category',on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField('Tag',related_name='article')
    brief_description = models.CharField(max_length=128,verbose_name='简介')
    content = RichTextField()
    allow_comment = models.BooleanField(default=True,verbose_name='是否允许评论')
    pub_date = models.DateTimeField(verbose_name='日期',auto_now_add=True)
    author = models.ForeignKey('WebUser',on_delete=models.CASCADE)
    viewed_number = models.IntegerField(verbose_name='查看数', default=0)
    raised_number = models.IntegerField(verbose_name='点赞数', default=0)


    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title



# 评论
class Comment(models.Model):
    article = models.ForeignKey('Article',on_delete=models.CASCADE, related_name='comment')
    parentComment = models.ForeignKey('Comment',related_name='descendantComment',blank=True,null=True,on_delete=models.CASCADE,verbose_name='父评论')
    observer = models.ForeignKey('WebUser',on_delete=models.CASCADE)
    content = RichTextField()
    sub_time = models.DateTimeField(verbose_name='提交时间')
    raised_point = models.IntegerField(default=0,verbose_name='点赞数')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
