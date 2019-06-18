## 用于配置gunicorn的脚本文件
#!/bin/bash

NAME="gunicorn_djangopro"    ##定义一个名字，用来作为进程名
DIR=/data/wwwroot/mutiSite    ##你的项目路径
USER=root   ##启动该项目使用的用户
GROUP=root ##启动该项目使用的用户的组
WORKERS=2 ## WORKERS是工作线程数，一般为cpu数+1
BIND=unix:/tmp/gunicorn.sock ##不需要你手工创建该文件！！！这是自动创建的用来通信的套接字
DJANGO_SETTINGS_MODULE=mysite.settings ##改成你的项目
DJANGO_WSGI_MODULE=mysite.wsgi ##改成你的项目
LOG_LEVEL=debug

cd $DIR
source /data/venv/mysite/bin/activate ## 激活虚拟环境
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DIR:$PYTHONPATH

##下面的/usr/local/bin/gunicorn  改成你自己安装后的gunicorn的路径，可以使用whereis gunicorn 来找到
exec /data/venv/mysite/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $WORKERS \
  --user=$USER \
  --group=$GROUP \
  --bind=$BIND \
  --log-level=$LOG_LEVEL \
  --log-file=/usr/local/bin/gunicorn.log # 需要事先创建log文件