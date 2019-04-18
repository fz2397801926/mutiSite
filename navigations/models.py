from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=32,verbose_name='名称')
    englishName = models.CharField(max_length=32,verbose_name='英文名称')
    iconfont = models.CharField(max_length=32,verbose_name='图标')
    private = models.BooleanField(verbose_name='隐藏')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Website(models.Model):
    name = models.CharField(max_length=32,verbose_name='名称')
    icon = models.ImageField(upload_to='navigations/icon/',blank=True,null=True,verbose_name='图标')
    url = models.URLField(max_length=128,verbose_name='网址')
    description = models.CharField(max_length=128,blank=True,null=True,verbose_name='描述')
    category = models.ForeignKey('Category',on_delete=models.CASCADE,related_name='website',verbose_name='分类')

    class Meta:
        verbose_name = '网站'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name