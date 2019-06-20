# 需要先运行proxypool
import requests

def get_proxy():
    PROXY_POOL_URL = 'http://localhost:5555/random'

    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


def count_proxy():
    PROXY_POOL_URL = 'http://localhost:5555/count'

    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None

if __name__ == '__main__':
    print(get_proxy())
    print(count_proxy())