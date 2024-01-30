import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = 'http://www.studyofnet.com//844378144.html'

    response = requests.get(url)
    response.encoding = 'utf8'
    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup)
    # print(soup.find('title').text)
    # print(soup.find('meta', attrs={'property': 'og:description'})['content'])
    for i in soup.find('div', class_='textcontent js_img_share_area').find_all('p'):
        # try:
        #     print(i.text.strip())
        #     print(i.find('p').text)
        # except:
        print(i.text.strip())
        # print('-'*100)
