# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc :
__coding__ = "utf-8"

import time

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import queue


def request_question(url_num):
    r = requests.get(url_num[0], headers=headers)
    r.encoding = 'utf8'
    soup = BeautifulSoup(r.text, 'lxml')
    question = soup.find('div', 'block')
    # 做html
    result_html = '<div class="page">'
    result_html += f"<p>{url_num[1]}、</p>\n"

    for i in question.find_all('p'):
        if i.text.strip() != '':
            result_html += f"<p>{i.text.replace(' ', '')}</p>\n"

        imgs = i.find_all('img')
        if len(imgs) != 0:
            for img in imgs:
                result_html += f"<img src='{img.get('src')}' alt='{img.get('alt')}'>\n"

    result_html += f"<p>{'==' * 30}</p>\n"
    result_html += '</div>\n'

    print(f"request question_ID:{url_num[1]} success!")
    result[url_num[1]] = result_html


with open('question.html', 'w', encoding='utf-8') as f:
    f.write("<!DOCTYPE html> <html> <head> <style> .page { display: none; page-break-after: always; } </style> </head> <body>\n")
    f.write("""
<div>
  <label for="pageInput">跳转到第</label>
  <input type="number" id="pageInput" min="1" max="1000">
  <label for="pageInput">页</label>
  <button onclick="jumpToPage()">跳转</button>
</div>
<script>
var totalPages = 50; // 总页数

// 在页面加载完成后显示第一个页面
window.onload = function() {
  showPage(0);
};

// 根据索引显示对应的页面块
function showPage(index) {
  var pages = document.getElementsByClassName("page");
  for (var i = 0; i < pages.length; i++) {
    if (i === index) {
      pages[i].style.display = "block";
    } else {
      pages[i].style.display = "none";
    }
  }
}

// 点击下一页按钮时，显示下一页
function nextPage() {
  var currentPage = document.querySelector(".page[style*='block']");
  var nextPage = currentPage.nextElementSibling;
  if (nextPage && nextPage.classList.contains("page")) {
    currentPage.style.display = "none";
    nextPage.style.display = "block";
  }
}

// 点击上一页按钮时，显示上一页
function prevPage() {
  var currentPage = document.querySelector(".page[style*='block']");
  var prevPage = currentPage.previousElementSibling;
  if (prevPage && prevPage.classList.contains("page")) {
    currentPage.style.display = "none";
    prevPage.style.display = "block";
  }
}

// 跳转到指定页数
function jumpToPage() {
  var input = document.getElementById("pageInput");
  var page = parseInt(input.value);
  if (!isNaN(page) && page >= 1 && page <= totalPages) {
    showPage(page - 1);
  }
}
</script>

<button onclick="prevPage()">上一页</button>
<button onclick="nextPage()">下一页</button>
    
    
""")

if __name__ == '__main__':
    timeStart = time.time()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    headers = {'User-Agent': user_agent}
    queue_list = queue.Queue()
    pool = ThreadPoolExecutor(max_workers=100)

    questionID_start = 270000
    questionID_end = 270050
    for i in range(questionID_start, questionID_end):
        url = f"http://czwl.cooco.net.cn/testdetail/{i}/"
        # url = f"http://cooco.net.cn/question/{i}.html"
        queue_list.put([url, i])

    result = {}
    for i in range(queue_list.qsize()):
        pool.submit(request_question, queue_list.get())

    while True:
        if queue_list.qsize() == 0:
            time.sleep(5)
            sorted_keys = sorted(result.keys())
            for key in sorted_keys:
                value = result[key]
                with open('question.html', 'a', encoding='utf-8') as f:
                    f.write(value)
            break
        time.sleep(1)

    with open('question.html', 'a', encoding='utf-8') as f:
        f.write("</body></html>")
    print(f'execute_time is {time.time()-timeStart}')