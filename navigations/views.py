from django.shortcuts import render
from navigations import models
# Create your views here.

def index(request):
    categoryList = models.Category.objects.all()
    for category in categoryList:
        websiteList = category.website.all()
        print(websiteList)
    return render(request,'navigations/index.html',locals())