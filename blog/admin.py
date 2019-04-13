from django.contrib import admin
from blog import models
# Register your models here.

class WebUserAdmin(admin.ModelAdmin):
    list_display = ('username',)

admin.site.register(models.WebUser, WebUserAdmin)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Comment)
admin.site.register(models.Article)