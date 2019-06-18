from django.contrib import admin
from blog import models
# Register your models here.


admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Drection)
admin.site.register(models.Classification)
admin.site.register(models.Level)
admin.site.register(models.Article)
admin.site.register(models.Resource)
admin.site.register(models.Comment)
admin.site.register(models.Picture)