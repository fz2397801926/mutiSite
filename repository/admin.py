from django.contrib import admin
from repository import models
# Register your models here.

class WebUserAdmin(admin.ModelAdmin):
    list_display = ('username',)

admin.site.register(models.WebUser, WebUserAdmin)
admin.site.register(models.ConfirmString)