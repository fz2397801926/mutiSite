"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog import views

# 命名空间，防止url别名混用
app_name = 'blog'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('list/<int:currentPage>', views.list_pages, name='list'),
    path('article/<int:id>', views.context, name='article'),
    path('resource/', views.resource, name='resouce'),
    path('error/', views.error, name='error'),

    path('upload.html', views.upload, name='upload'),




    path('test.html', views.test, name='test'),
    path('img.html', views.img, name='img'),
    path('get_img.html', views.get_img),
    path('markdown.html', views.markdown),

    path('ajax.html', views.ajax, name='ajax'),
    path('adduser/', views.addUser),
    path('addarticle/', views.addArticle),
]
