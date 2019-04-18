import datetime
from django.core.mail import EmailMultiAlternatives,send_mail
from blog.models import *
from mysite import settings
from utils.encryption import hashEncrypt

def makeConfirmCode(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hashEncrypt(user.username, now)
    ConfirmString.objects.create(code=code, user=user,)
    return code

def sendEmail(email,code):
    subject = '注册确认'
    text_content = '欢迎注册访问一只麻瓜的博客'
    html_content = '''
                    <p>感谢注册<a href="http://{}/blog/confirm/?code={}" target=blank>一只麻瓜的博客</a></p>
                    <p>请点击站点链接完成注册确认。</p>
                    <p>此链接有效期为{}天。</p>
                    '''.format(settings.HOST_IP, code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email,])
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
        print('done')
        status = 'success'
    except Exception:
        status = 'fail'
    return status





