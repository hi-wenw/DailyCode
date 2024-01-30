# 请求URL
import requests
from bs4 import BeautifulSoup

url = 'https://www.shanghairanking.cn/rankings/bcur/2023'
# 请求头部
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

if __name__ == '__main__':
    response = requests.get(url, headers)
    response.encoding = 'utf8'
    soup = BeautifulSoup(response.text, "html.parser")
    for row in soup.find('table', class_='rk-table').find_all('tr')[1:]:
        cols = row.find_all("td")
        ranking = cols[0].text.strip()
        name = cols[1].find("a").text.strip()
        tags = cols[1].find("p", class_="tags").text.strip()
        location = cols[2].text.strip()
        category = cols[3].text.strip()
        score = cols[4].text.strip()
        print(ranking, name, tags, location, category, score)

    # print(soup.find('table', class_='rk-table').find_all('tr')[1].find_all("td")[0])
    # print('-'.center(100, '-'))
    # print(soup.find('table', class_='rk-table').find_all('tr')[1].find_all("td")[1])
    # print('-'.center(100, '-'))
    # print(soup.find('table', class_='rk-table').find_all('tr')[1].find_all("td")[2])
    # print('-'.center(100, '-'))
    # print(soup.find('table', class_='rk-table').find_all('tr')[1].find_all("td")[3])
    # print('-'.center(100, '-'))
    # print(soup.find('table', class_='rk-table').find_all('tr')[1].find_all("td")[4])
