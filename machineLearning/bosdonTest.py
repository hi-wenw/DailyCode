import requests

url = "https://eolink.o.apispace.com/456456/weather/v001/day"

payload = {"days" : "30","areacode" : "101010100","lonlat" : "116.407526,39.904030"}

headers = {
    "X-APISpace-Token":"lp8d8zt893qzk0gjzb5ca3u1gnj9symh",
    "Authorization-Type":"apikey"
}

response=requests.request("GET", url, params=payload, headers=headers)

print(response.text)
