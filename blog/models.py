from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.


# 用户
class WebUser(models.Model):
    gender = {
        ('male','男'),
        ('female','女'),
        ('unkown','保密'),
    }

    username = models.CharField(max_length=20, verbose_name='名称')
    password = models.CharField(max_length=20, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')
    sex = models.CharField(max_length=32,choices=gender)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

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
    content = RichTextField()
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
    article = models.ForeignKey('Article',on_delete=models.CASCADE, default=None, related_name='comment')
    observer = models.ForeignKey('WebUser',on_delete=models.CASCADE)
    content = models.TextField()
    sub_time = models.DateTimeField()
    raised_point = models.IntegerField(verbose_name='点赞数', default=0)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
