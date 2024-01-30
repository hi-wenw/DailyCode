# 导入requests库
import requests

# -------------------------------------------------------------------------
# # 发送一个get请求并得到响应
# r = requests.get('https://www.baidu.com')
# # 查看响应对象的类型
# print(type(r))
# # 查看响应状态码
# print(r.status_code)
# # 查看响应内容的类型
# print(type(r.text))
# # 查看响应的内容
# print(r.text)
# # 查看cookies
# print(r.cookies)

# -------------------------------------------------------------------------
# 请求参数
# data = {'name': 'baozi', 'age': 22}
# # r = requests.get('http://httpbin.org/get', params=data)
# r = requests.post('http://httpbin.org/post',data=data)
#
# print(r.text)


# -------------------------------------------------------------------------
# 请求头
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
#     'my-test': 'Hello'
# }
# r = requests.get('http://httpbin.org/get', headers=headers)
# print(r.text)
#
# # 响应内容（str类型）
# print(type(r.text), r.text)
# # 响应内容（bytes类型）
# print(type(r.content), r.content)
# # 状态码
# print(type(r.status_code), r.status_code)
# # 响应头
# print(type(r.headers), r.headers)
# # Cookies
# print(type(r.cookies), r.cookies)
# # URL
# print(type(r.url), r.url)
# # 请求历史
# print(type(r.history), r.history)

# -------------------------------------------------------------------------
# 爬二进制
# r = requests.post('https://www.baidu.com/favicon.ico')
# with open('photo.ico', 'wb') as f:
#     f.write(r.content)
#
# # 以二进制方式读取当前目录下的favicon.ico文件，并将其赋给file
# files = {'file': open('photo.ico', 'rb')}
# # 进行上传
# print(files)
# r = requests.post('http://httpbin.org/post', files=files)
# print(r.text)

# -------------------------------------------------------------------------


r = requests.get('https://www.baidu.com')
# 打印Cookies对象
print(r.cookies)
# 遍历Cookies
for key, value in r.cookies.items():
    print(key + '=' + value)
