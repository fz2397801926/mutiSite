from django.shortcuts import render,HttpResponse
from utils import proxyOperater

# Create your views here.

def get_proxy(request):
    proxy = proxyOperater.get_proxy()
    return HttpResponse(proxy)

def proxy_number(request):
    number = proxyOperater.count_proxy()
    return HttpResponse(number)