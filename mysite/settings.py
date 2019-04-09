"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^ckwk_b6+zo@)86_z0c(oncgkg#qced6p1ei4jt09idh44jaiw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 邮件通知
ADMINS = (
('amagua','2397801926@qq.com'),
)
# 邮件通知
MANAGERS = (
('amagua', '2397801926@qq.com'),
)


ALLOWED_HOSTS = ['127.0.0.1','47.98.127.54',]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'navigations',
    'aria',
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# mysql数据库
DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.mysql',

        'NAME': 'mysite',    #你的数据库名称

        'USER': 'root',   #你的数据库用户名

        'PASSWORD': '123456', #你的数据库密码

        'HOST': '', #你的数据库主机，留空默认为localhost

        'PORT': '3306', #你的数据库端口

    }

}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR,"blog/static/"),
    os.path.join(BASE_DIR,"navigations/static/"),
]



# upload folder
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')


# # 调试模式
# if DEBUG:
#
#
# # django debug toolbar
#     INSTALLED_APPS.append('debug_toolbar')
#     MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
#     DEBUG_TOOLBAR_CONFIG = {
#         'JQUERY_URL': '//cdn.bootcss.com/jquery/2.1.4/jquery.min.js',
#         # 或把jquery下载到本地然后取消下面这句的注释, 并把上面那句删除或注释掉
#         #'JQUERY_URL': '/static/jquery/2.1.4/jquery.min.js',
#         'SHOW_COLLAPSED': True,
#         'SHOW_TOOLBAR_CALLBACK': lambda x: True,
#     }
# # 允许使用的主机
# INTERNAL_IPS = ['127.0.0.1']