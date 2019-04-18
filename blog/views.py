import datetime
from django.shortcuts import render,HttpResponse,redirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from io import BytesIO
from mysite.mypaginator import MyPaginator
from mysite import settings
from blog.models import *
from blog.blogForms import *
from utils.check_code import create_validate_code
from utils.encryption import hashEncrypt
from utils.sendEmail import sendEmail,makeConfirmCode
# Create your views here.



# 主页
def index(request):
    userform = LoginForm()
    categoryList = Category.objects.all()
    paginator = MyPaginator(1, 10, Article.objects.all(), 5)
    try:
        postPage = paginator.page(1)
    except PageNotAnInteger:
        postPage = paginator.page(1)
    except EmptyPage:
        postPage = paginator.page(paginator.num_pages)
    return render(request, 'blog/index.html',{'postPage':postPage,'categoryList':categoryList,'userform':userform})

# 列表页
def list(request,currentPage):
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

# 验证码
def checkCode(request):
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())

# 登录页
def login(request):
    if request.session.get('is_login', None):
        return redirect("blog/index/")
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        message = "请检查填写的内容！"
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            try:
                user = WebUser.objects.get(username=username)
                if not user.has_confirmed:
                    message = "该用户还未通过邮件确认！"
                    return render(request, 'blog/login.html', locals())
                if user.password == hashEncrypt(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    return redirect('/blog/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
            return render(request, 'blog/login.html', locals())
        else:
            loginForm =LoginForm()
            return render(request, 'blog/login.html', locals())
    else:
        loginForm = LoginForm()
        return render(request, 'blog/login.html', locals())

# 注册页
def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("blog/index/")
    if request.method == 'POST':
        registerForm = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if registerForm.is_valid():  # 获取数据
            username = registerForm.cleaned_data['username']
            password = registerForm.cleaned_data['password']
            passwordConfirmed = registerForm.cleaned_data['passwordConfirmed']
            email = registerForm.cleaned_data['email']
            sex = registerForm.cleaned_data['sex']
            if password != passwordConfirmed:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'blog/register.html', locals())
            else:
                same_name_user = WebUser.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'blog/register.html', locals())
                same_email_user = WebUser.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'blog/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = WebUser()
                new_user.username = username
                new_user.password = hashEncrypt(password)  # 使用加密密码
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = makeConfirmCode(new_user)
                sendEmail(email, code)

                message = '请前往注册邮箱，进行邮件确认！如果没有收到邮件，请在垃圾箱中查看'
                return render(request, 'blog/register.html', locals())  # 跳转到等待邮件确认页面。
    else:
        registerForm = RegisterForm()
        return render(request, 'blog/register.html', locals())

# 用户注册确认
def userConfirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'blog/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()

    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'blog/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'blog/confirm.html', locals())

# 注销
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/blog/index/")
    request.session.flush()
    return redirect("/blog/index/")

def background(request):
    editForm = EditForm()
    loginForm = LoginForm()
    return render(request,'blog/userBackgroud.html',locals())

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

