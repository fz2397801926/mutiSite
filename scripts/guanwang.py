import requests
from bs4 import BeautifulSoup

def getData():
    # 获取老师名单
    for i in range(1,5):
        # print('123%d',)
        res = requests.get('http://zs.yjs.cqut.edu.cn/dslist.jsp?a131049t=4&a131049p='+ str(i) +'&a131049c=20&urltype=tree.TreeTempUrl&wbtreeid=1648')
        print(res)
        beau = BeautifulSoup(res.content,'html.parser')
        content = beau.select('#container-right .list a')
        print(content.select('href'))
        print(content.selct(''))
    # 获取详细信息


getData()