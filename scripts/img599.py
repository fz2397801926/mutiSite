import requests
import time
import os
import base64
from bs4 import BeautifulSoup

def imgEncode(path):
    imgDic = {
        'imgSize': '',
        'imgData':'',
    }
    imgDic['imgSize'] = os.path.getsize(path)
    with open(path,'rb') as f:
        imgDic['imgData'] = base64.b64encode(f.read())
    return imgDic

# 登录
def login(userData):
    url = 'http://img599.net/login'
    headers = {
        'Host': 'img599.net',
        'Origin': 'http://img599.net',
        'Referer': 'http://img599.net/',
        'Upgrade-Insecure-Requests': '1',
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    loginData = {
        'auth_token': '6e9b04f30322f80001692f2a5743b23eb7bd2978',
        'login-subject': userData['username'],
        'password': userData['password'],
        'keep - login': '1',
    }

    session = requests.session()
    resp = session.post(url=url,headers=headers,data=loginData)
    print(resp.status_code)

    return session

# 上传，暂时失败
def upload(session,imgDic):
    # 暂时失败
    url = 'http://img599.net/json'
    timestamp= int(round(time.time()*1000))
    imgData = imgDic['imgData']
    imgSize = imgDic['imgSize']
    headers = {
        'Content-Length': str(imgSize),
        'Content - Type': 'image3/png',
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    data = {
        'source': imgData,
        'type': 'file',
        'action': 'upload',
        'privacy': 'null',
        'timestamp': str(timestamp),
        'auth_token': '6e9b04f30322f80001692f2a5743b23eb7bd2978',
        'category_id': 'null',
        'nsfw': '1',
        'album_id': 'null',
    }

    resopnse = session.post(url=url,headers=headers,data=data)
    return resopnse

def getImg(session,username):
    # 获取相册目录

    url = 'http://img599.net/'+str(username)+'/albums'
    respose = session.get(url)
    print(BeautifulSoup(respose.content,'html.parser'))
    # 进入相册，获取图片链接

    # 对图片进行排序

if __name__ == "__main__":

    userData = {
        'username':'amagua',
        'password':'cpt1bt2ptp3'
    }

    # imgPath = 'C:\\Users\\23978\\Desktop\\123.jpg'
    #
    # imgDic = imgEncode(imgPath)

    # session = login()
    # resopnse = upload(session,imgDic)

    session = login(userData)
    url = 'http://img599.net/'
    respose = session.get(url)
    with open('1.html','w') as f:
        f.write(BeautifulSoup(respose.content,'html.parser').text)
