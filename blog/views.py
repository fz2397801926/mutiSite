import datetime

from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from mysite.mypaginator import MyPaginator
from blog.models import *

# Create your views here.


# 主页
def index(request):
    categoryList = Category.objects.all()
    paginator = MyPaginator(1, 10, Article.objects.all(), 5)
    try:
        postPage = paginator.page(1)
    except PageNotAnInteger:
        postPage = paginator.page(1)
    except EmptyPage:
        postPage = paginator.page(paginator.num_pages)
    return render(request, 'blog/index.html',{'postPage':postPage,'categoryList':categoryList})

# 列表页
def list_pages(request,currentPage):
    categoryList = Category.objects.all()
    tagList = Tag.objects.all()
    # 分页
    paginator = MyPaginator(currentPage,10,Article.objects.all(),5)
    try:
        postPage = paginator.page(currentPage)
    except PageNotAnInteger:
        postPage = paginator.page(1)
    except EmptyPage:
        postPage = paginator.page(paginator.num_pages)
    return render(request, 'blog/list.html', {'categoryList':categoryList,'tagList':tagList,'postPage':postPage})

# 详情页
def context(request,id):
    return_dic = {}
    return_dic['categoryList'] = Category.objects.all()
    return_dic['article'] = Article.objects.get(id=id)
    return_dic['comment_list'] = Comment.objects.all().order_by('-id')
    if request.method == 'POST':
        content = request.POST.get('comment-textarea')
        artile_id = request.POST.get('article_id')
        user_id = request.session.get('user_id')
        user = WebUser.objects.get(id=user_id)
        sub_time = datetime.datetime.now()
        try:
            Comment.objects.create(article=return_dic['article'],observer=user,content=content,sub_time=sub_time)
            return_dic['status'] = 'success'
        except Exception:
            return_dic['status'] = 'false'
        return render(request, 'blog/article.html',return_dic)
    return render(request, 'blog/article.html',return_dic)



def resource(request):
    return render(request, 'blog/resource.html',)



# 错误页
def error(request):
    return render(request, 'blog/error.html')

# 上传
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

    users = WebUser.objects.all()

    return render(request, 'blog/test.html',{'users':users,})


def img(request):
    img_cols = 4
    img_list = Picture.objects.all()

    return render(request, 'blog/img.html',{'img_list':img_list,'img_cols':img_cols})

def get_img(request):
    img_list = list(Picture.objects.values('id','title','local_path','net_src'))

    ret = {
        'status':'success',
        'data':img_list,
    }

    return JsonResponse(ret)

def markdown(request):
    return render(request,'blog/markdown.html')

def ajax(request):
    print(request.GET)
    print(request.POST)
    return HttpResponse('status')


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

