# 请求URL
import requests

url = 'https://www.maoyan.com/board/4?offset='
# 请求头部
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}

offset = 0

response = requests.get(url + str(offset))
response.encoding = 'utf8'
print(response.text)
