import os
import json
from django.shortcuts import render,HttpResponse
from mysite.settings import BASE_DIR,systemType
from utils.operateFiles import sortFile
# Create your views here.

# 主页
def index(request):
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
    return render(request, 'yunfile/index.html',{'dirList':dirList,'fileList':fileList,'currentPath':toPath})

# 文件列表页
def listFile(request):
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
    return render(request, 'yunfile/fileDetail.html', {'relativePath':relativePath, 'suffix':suffix, 'fileList':fileList, })

