import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    response = requests.request('GET', 'https://baike.baidu.com/item/%E7%85%B2%E4%BB%94%E9%A5%AD/6013357?fr=ge_ala')
    soup = BeautifulSoup(response.text, "html.parser")
    img = soup.find_all("img")
    print(soup)
