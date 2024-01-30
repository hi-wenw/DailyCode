import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # 主页
    url = 'http://www.studyofnet.com/'
    response = requests.get(url)
    response.encoding = 'utf8'

    # 解析热门前10,获取排名及标题及链接
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find_all('div', class_='m-cont-right g-rank-li f-fr')[-1].find_all('li')
    ls = []
    for i in title:
        col0 = i.find('span').text
        col1 = i.find('a')['href']
        col2 = i.find('a').text
        ls.append([col0, col1, col2])

    # 爬取对应标题内的内容 并写入至data目录下
    for j in ls:
        new_url = url + j[1]
        new_response = requests.get(new_url)
        new_response.encoding = 'utf8'
        soup = BeautifulSoup(new_response.text, 'lxml')
        with open(f'data/{str(j[0] + j[2])}.txt', 'w', encoding='utf-8') as f:
            for k in soup.find('div', class_='textcontent js_img_share_area').find_all('p'):
                f.write(k.text.strip())
                f.write('\n')
