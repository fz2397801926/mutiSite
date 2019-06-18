from django.db import models
from ckeditor.fields import RichTextField

from repository.models import WebUser
# Create your models here.




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


# 方向
class Drection(models.Model):
    name = models.CharField(max_length=32, verbose_name='名称')

    class Meta:
        verbose_name = '教程方向'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 分类
class Classification(models.Model):
    name = models.CharField(max_length=32, verbose_name='名称')

    class Meta:
        verbose_name = '教程分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 等级
class Level(models.Model):
    name = models.CharField(max_length=32, verbose_name='名称')

    class Meta:
        verbose_name = '教程等级'
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
    author = models.ForeignKey(WebUser,on_delete=models.CASCADE)
    viewed_number = models.IntegerField(verbose_name='查看数', default=0)
    raised_number = models.IntegerField(verbose_name='点赞数', default=0)


    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

# 资源链接
class Resource(models.Model):
    title = models.CharField(max_length=20,default=None,verbose_name='标题')
    drection = models.ForeignKey('Drection',on_delete=models.CASCADE,null=True)
    classification = models.ForeignKey('Classification',on_delete=models.CASCADE,null=True)
    Level = models.ForeignKey('Level',on_delete=models.CASCADE,null=True)
    article = models.ForeignKey('Article',on_delete=models.CASCADE, related_name='resource')
    content = RichTextField()
    from_website = models.URLField(verbose_name='原网址')

    class Meta:
        verbose_name = '教程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

# 评论
class Comment(models.Model):
    article = models.ForeignKey('Article',on_delete=models.CASCADE, related_name='comment')
    parentComment = models.ForeignKey('Comment',related_name='descendantComment',blank=True,null=True,on_delete=models.CASCADE,verbose_name='父评论')
    observer = models.ForeignKey(WebUser,on_delete=models.CASCADE)
    content = RichTextField()
    sub_time = models.DateTimeField(verbose_name='提交时间')
    raised_point = models.IntegerField(default=0,verbose_name='点赞数')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name


# 图片
class Picture(models.Model):
    local_path = models.ImageField(max_length=32, verbose_name='本地路径',blank=True)
    net_src = models.URLField(max_length=32, verbose_name='网络地址',blank=True)
    title = models.CharField(max_length=32, verbose_name='标题')
    summary = models.CharField(max_length=128, verbose_name='描述')

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title