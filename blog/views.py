import os
from django.shortcuts import render,HttpResponse,redirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib import auth
from mysite.settings import BASE_DIR,systemType
from io import BytesIO
from blog.models import *
from mysite.mypaginator import MyPaginator
from blog.blogForms import *
from utils.check_code import create_validate_code
from utils.operateFiles import sortFile
# Create your views here.



# 主页
def index(request):
    userform = LoginForm()
    user = request.user
    paginator = MyPaginator(1, 10, Article.objects.all(), 5)
    try:
        postPage = paginator.page(1)
    except PageNotAnInteger:
        postPage = paginator.page(1)
    except EmptyPage:
        postPage = paginator.page(paginator.num_pages)
    return render(request, 'blog/index.html',{'user':user,'postPage':postPage,'userform':userform})

# 列表页
def list(request,currentPage):
    category = Category.objects.all()
    tagList = Tag.objects.all()
    # 分页
    paginator = MyPaginator(currentPage,10,Article.objects.all(),5)
    try:
        postPage = paginator.page(currentPage)
    except PageNotAnInteger:
        postPage = paginator.page(1)
    except EmptyPage:
        postPage = paginator.page(paginator.num_pages)
    return render(request, 'blog/list.html', {'category':category,'tagList':tagList,'postPage':postPage})

# 详情页
def context(request,id):
    artile = Article.objects.get(id=id)
    return render(request, 'blog/article.html',{'article':artile})

# 验证码
def checkCode(request):
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())

# 登录页
def login(request):
    if request.method == 'GET':
        loginForm = LoginForm()
        return render(request, 'blog/login.html', {'loginForm': loginForm})
    elif request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            print(username)
            print(password)
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request,user)
                return redirect('')
            return render(request, 'blog/login.html', {'status': 'success'})
        else:
            return render(request, 'blog/login.html', {'loginForm': loginForm})

# 注册页
def register(request):
    if request.method == 'GET':
        registerForm = RegisterForm()
        return render(request, 'blog/register.html', {'registerForm': registerForm,'checckError':'验证码输入错误'})
    else:
        registerForm = RegisterForm(request.POST)
        print(request.POST)
        print(request.POST.get('checkCode'))
        print(request.session['CheckCode'])
        if request.POST.get('checkCode') != request.session['CheckCode']:
            return render(request, 'blog/register.html', {'registerForm': registerForm})
        if registerForm.is_valid():
            print('success')
        return render(request, 'blog/register.html', {'registerForm': registerForm})


# 错误页
def error(request):
    return render(request, 'blog/error.html')


def upload(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        file = request.FILES.get('files')
        with open(file.name,'wb') as f:
            for line in file.chunks():
                f.write(line)
        return render(request,'blog/test.html')

def test(request):
    from urllib.parse import quote,unquote

    users = WebUser.objects.all()

    MEDIA_DIR = os.path.join(BASE_DIR,'media')
    # 获取当前路径
    toPath = request.GET.get('path')
    # 无参数时
    if toPath == None:
        toPath = ''
        currentPath = MEDIA_DIR
    # 有参数时
    else:
        if systemType == 'WindowsPE':
            # windows需要转换分隔符
            currentPath = MEDIA_DIR + toPath.replace('/','\\')
        else:
            # linux
            currentPath = MEDIA_DIR + toPath
        print(currentPath)
    # 获取文件
    searchResult = os.listdir(currentPath)
    # 文件和文件夹列表
    fileList = []
    dirList = []
    for result in searchResult:
        if os.path.isdir(os.path.join(currentPath,result)):
            dirList.append(result)
        elif os.path.isfile(os.path.join(currentPath,result)):
            fileList.append(result)
    return render(request, 'blog/test.html',{'users':users,'dirList':dirList,'fileList':fileList,'currentPath':toPath})

# 解压文件
def unzipFile(request):
    import json
    from utils.operateFiles import unzipFile,decom7zFile

    MEDIA_DIR = os.path.join(BASE_DIR, 'media')
    print(request.GET)
    print(request.POST)
    fileList = json.loads(request.POST.get('fileList'))
    resultList = []
    for file in fileList:
        if systemType == 'WindowsPE':
            # windows转换分隔符
            file = file.replace('/','\\')
        # 去空格
        stripedFile = file.replace(' ','')
        os.rename(MEDIA_DIR + file,MEDIA_DIR + stripedFile)
        filePath = MEDIA_DIR + stripedFile
        print(filePath)
        print(filePath.split('.')[1])
        status = 'success'
        if filePath.split('.')[1] == 'zip':
            status = unzipFile(filePath)
        elif filePath.split('.')[1] == '7z':
            status = decom7zFile(filePath)
        result = file + str(status)
        resultList.append(result)
    resultList = json.dumps(resultList)
    return HttpResponse(resultList)

# 文件详情页
def fileDetail(request):
    print(request.GET)

    if systemType == 'WindowsPE':
        # windows替换分隔符
        relativePath = request.GET.get('path').replace('/','\\')[1:]
    else:
        relativePath = request.GET.get('path')[1:]

    currentPath = os.path.dirname(relativePath)
    absolutePath = os.path.join(BASE_DIR, os.path.join('media', relativePath))
    print(currentPath)
    print(relativePath)
    print(absolutePath)
    suffix = absolutePath.split('.')[1]
    fileDir = os.path.dirname(absolutePath)
    fileList = []
    for file in sortFile(os.listdir(fileDir)):
        # 文件信息
        fileDetail = {}
        # 文件绝对路径
        filePath = os.path.join(fileDir,file)
        if os.path.isfile(filePath):
            fileDetail['relativePath'] = os.path.join(currentPath,file)
            fileDetail['fileName'] = os.path.split(filePath)[1]
            fileDetail['suffix'] = filePath.split('.')[1]
            print(fileDetail)
            fileList.append(fileDetail)
    return render(request,'blog/fileDetail.html',{'relativePath':relativePath,'suffix':suffix,'fileList':fileList,})


def ajax(request):
    print(request.GET)
    print(request.POST)
    return HttpResponse('status')

def listFile(request):
    import os
    import json
    print(request.GET)
    # 当前目录
    currentDir = request.GET.get('currentDir')
    print(currentDir)
    # 根目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 媒体目录
    mediaDir = os.path.join(BASE_DIR, 'media')
    if currentDir == None:
        currentDir = mediaDir
    elif currentDir == 'parentDir':
        currentDir = os.path.dirname(currentDir)
    fileList = json.dumps(os.listdir(currentDir))
    return HttpResponse(fileList)

def addUser(requset):
    WebUser.objects.create(username='ava', password='123456', email='123@qq.com',sex='女')

    return HttpResponse('add ok')

def addArticle(requset):
    categoryObj = Category.objects.all().first()
    tagObj = Tag.objects.all().first()
    authorObj = WebUser.objects.all().first()
    for i in range(30):
        Article.objects.create(title='ava', category=categoryObj,author=authorObj)

    return HttpResponse('add ok')