import requests
from bs4 import BeautifulSoup
def getData():
    url = 'https://yz.chsi.com.cn/sytj/stu/tjyxqexxcx.action'
    header = {
        'User-Agent':'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 72.0.3626.121Safari / 537.36',
    }
    formData = {
        'pageSize': '60',
        'start': '0',
        'orderBy':'',
        'ssdm': '51',
        'dwmc':'',
        'xxfs': '1',
        'zymc': '机械工程',
        'data_type': 'json',
        'agent_from': 'web',
        'pageid': 'tjyx_qe_list',
    }

    res = requests.post(url=url,data=formData)
    print(BeautifulSoup(res.content,'html.parser'))


if __name__ == '__main__':
    data = getData()