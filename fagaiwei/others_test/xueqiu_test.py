import requests

# url = "http://news.people.com.cn/210801/211150/index.js?_=1525332714933"
url = "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&max_id=-1&count=10&category=111"
headers = {
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Accept-Language": "zh-CN,zh;q=0.9",
    # "Cache-Control": "max-age=0",
    # "Connection": "keep-alive",
    # "Host": "xueqiu.com",
    # "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
}
st_url = "https://xueqiu.com/"
session = requests.session()
res = session.get(st_url, headers=headers)
response = session.get(url, headers=headers)
print(response)
# print(response.json())
result = response.json()
print(result)

