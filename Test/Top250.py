import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # 请求URL
    url = 'https://movie.douban.com/top250?start='
    # 请求头部
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    for i in range(10):
        r = requests.get(url=url + str(i * 25), headers=headers)
        # print(r.text)
        soup = BeautifulSoup(r.text, 'lxml')
        movie_list = soup.find('ol', class_='grid_view').find_all('li')

        for movie in movie_list:
            title = movie.find('div', class_='hd').find('span', class_='title').get_text()
            rating_num = movie.find('div', class_='star').find('span', class_='rating_num').get_text()
            comment_num = movie.find('div', class_='star').find_all('span')[-1].get_text()

            print(title, rating_num, comment_num)
