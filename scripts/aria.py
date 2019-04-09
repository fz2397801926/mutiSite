import requests
import time
ariaurl="http://localhost:6800/jsonrpc"
dlurl= '' #文件真实路径
fn="bilan.7z"   #落地的文件名，
dn="D:\software\download\aria2-1.34.0-win-64bit-build1\file"      #本地目录
maxdowns=3    #最大并发数

#jsondata  rpc调用的数据头（固定部分）
jsondata={
    "jsonrpc":"2.0",
    "id":"qwer",
    "method":'',
    'params':[[],{}]
    }

def tellActive():
    status = ''
    reqdata = jsondata
    reqdata["method"] = "aria2.tellActive"  # aria  取当前并发数的的方法
    ret = requests.post(ariaurl, json=reqdata)
    # print(ret.json())
    curdowns = len(ret.json()["result"])
    if curdowns >= maxdowns:
        print("Busy,Waitting for links...")
        status = 'busy'
    else:
        print('kongxian')
        status = 'empty'
    return status

def ariadown(url,fname,fdir):          #url  是下载文件的链接，fname和fdir分别为本地文件名和目录
    reqdata=jsondata
    # reqdata["method"] = "aria2.tellActive"             #aria  取当前并发数的的方法
    # ret = requests.post(ariaurl, json=reqdata)
    # #print(ret.json())
    # curdowns=len(ret.json()["result"])
    # while curdowns >= maxdowns:
    #     print("Waitting for links...")
    #     time.sleep('2')                  #等不到就睡一觉
    #     ret = requests.post(ariaurl, json=reqdata)
    #     curdowns=len(ret.json()["result"])
    reqdata["method"] = "aria2.addUri"            #aria  增加下载的方法
    # reqdata['params'] = [[],{}]
    reqdata['params'][0] = [url]
    reqdata['params'][1] = {"out" : fname,"dir" : fdir}
    ret = requests.post(ariaurl, json=reqdata)
    return(ret.status_code)
# ret = ariadown(dlurl,fn,dn)                      #下载的调用
# print(ret)                       #是不是200？

if __name__ == '__main__':
    reqdata = jsondata
    status = tellActive()
    while status == 'busy':
        status = tellActive()
    if status == 'empty':
        ret = ariadown(dlurl, fn, dn)
        print(ret)

