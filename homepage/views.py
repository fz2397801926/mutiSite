import datetime

from io import BytesIO
from multiprocessing import Process
from django.shortcuts import render,redirect,HttpResponse

from mysite import settings
from homepage.forms import *
from repository.models import *
from utils.check_code import create_validate_code
from utils.encryption import hashEncrypt
from homepage.utils.sendEmail import sendEmail
# Create your views here.

# 主页
def index(request):
    if request.session.get('is_login',None):
        username = request.session['username']
    return render(request, 'homepage/index.html',locals())

# 登录页
def login(request):
    refer = request.POST.get('refer',None)
    if not refer:
        refer = request.META.get('HTTP_REFERER',None)
    print(refer)
    if request.session.get('is_login', None):
        return redirect(refer)
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        message = "请检查填写的内容！"
        if loginForm.is_valid():
            print('valid')
            email = loginForm.cleaned_data['email']
            password = loginForm.cleaned_data['password']
            try:
                user = WebUser.objects.get(email=email)
                if not user.has_confirmed:
                    message = "该用户还未通过邮件确认！"
                    print(message)
                    return render(request, 'homepage/login.html', locals())
                if user.password == hashEncrypt(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    print('success')
                    return redirect(refer)
                else:
                    message = "密码不正确！"
                    print(message)
            except:
                message = "用户不存在！"
                print(message)
            return render(request, 'homepage/login.html', locals())
        else:
            loginForm =LoginForm()
            return render(request, 'homepage/login.html', locals())
    else:
        loginForm = LoginForm()
        return render(request, 'homepage/login.html', locals())



# 注册页
def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect(request.path)
    if request.method == 'POST':
        registerForm = RegisterForm(request.POST)
        message = None
        if registerForm.is_valid():  # 获取数据
            username = registerForm.cleaned_data['nickname']
            email = registerForm.cleaned_data['email']
            password = registerForm.cleaned_data['password']
            passwordConfirmed = registerForm.cleaned_data['passwordConfirmed']
            if password != passwordConfirmed:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                print(message)
                return render(request, 'homepage/register.html', locals())
            else:
                same_email_user = WebUser.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    print(message)
                    return render(request, 'homepage/register.html', locals())

                # 当一切都OK的情况下，创建新用户
                new_user = WebUser()
                new_user.username = username
                new_user.password = hashEncrypt(password)  # 使用加密密码
                new_user.email = email
                new_user.save()

                code = makeConfirmCode(new_user)
                # sendEmail(email,code)
                sendEmailProcess = Process(target=sendEmail, args=(email, code))
                sendEmailProcess.start()

                message = '请前往注册邮箱，进行邮件确认！如果没有收到邮件，请在垃圾箱中查看'
                print(message)
                return render(request, 'homepage/info.html', locals())  # 跳转到等待邮件确认页面。
    else:
        registerForm = RegisterForm()
        return render(request, 'homepage/register.html', locals())

# 生成确认码
def makeConfirmCode(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hashEncrypt(user.username, now)
    ConfirmString.objects.create(code=code, user=user,)
    return code


# 注销
def logout(request):
    print(request.META.get('HTTP_REFERER',None))
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect(request.path)
    request.session.flush()
    return redirect(request.META.get('HTTP_REFERER',None))

# 验证码
def checkCode(request):
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())

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
        return render(request, 'homepage/confirm.html', locals())

# 用户后台
def userBackground(request):
    editForm = EditForm()
    loginForm = LoginForm()
    return render(request,'homepage/userBackground.html',locals())