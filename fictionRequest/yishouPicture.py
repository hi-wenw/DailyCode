import os

import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = 'https://www.baidu.com/s?ie=UTF-8&wd=%E5%8C%85%E5%AD%90'
    dir_name = 'baozi'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
    response = requests.get(url, headers=headers)

    response.encoding = 'utf8'

    soup = BeautifulSoup(response.text, 'lxml')

    all_images = soup.find_all('img')

    if response.status_code == 200:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    for image in all_images:
        img_url = image.get('src')
        if img_url.startswith(('http://', 'https://', '//')):
            if img_url.startswith('//'):
                img_url = f'https:{img_url}'
            img_name = img_url.split('/')[-1]
            img_path = os.path.join(dir_name, img_name)

            img_response = requests.get(img_url, headers=headers)
            with open(img_path, 'wb') as f:
                f.write(img_response.content)
                print(f'Saved image: {img_path}')
        else:
            print('Failed to retrieve the webpage.')
