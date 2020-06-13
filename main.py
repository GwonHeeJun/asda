import re
import requests
import json
from bs4 import BeautifulSoup
import time

start = time.time() 

keyword="the secret method of fitting a rodo"

def removeTag(content): # 영문 태그 다 없애주는 함수
   cleanr =re.compile('<([a-zA-Z]*)(\\s[a-zA-Z]*=[^>]*)?(\\s)*?>')
   cleantext = re.sub(cleanr, '', content)
   return cleantext

def removeZeroSpace(content): # Zero Space 유니코드 없애주는 함수
    cleanr = re.compile("[\\u200b[a-zA-Z]")
    cleantext = re.sub(cleanr, '', content)
    return cleantext

def getFristBlog(kwd): # 블로그 최상단 게시글 스크랩 
    manufKwd = str(kwd.encode('utf-8'))[2:] # 키워드 1차 가공
    realManufKwd = manufKwd[:-1].replace(r"\x", '%') # 키워드 2차 가공
    headers = {'Referer': 'https://section.blog.naver.com/Search/Post.nhn?pageNo=1&rangeType=ALL&orderBy=sim&keyword='+realManufKwd} # 오류 방지를 위한 헤더
    URL = 'https://section.blog.naver.com/ajax/SearchList.nhn?countPerPage=7&currentPage=1&endDate=&keyword='+realManufKwd+'&orderBy=sim&startDate=&type=post'
    response = requests.get(URL, headers=headers) # GET.
    resT = response.text[5:]
    resJ = json.loads(resT)
    return resJ["result"]["searchList"][0]["postUrl"] # 게시글 반환

def getBlogContent(uri): # 블로그 내용 스크랩
    payload = {"title" : "", "contents" : ""}
    print(uri)
    response = requests.get(uri.replace("https://", "https://m."))
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.select(
        '.se-main-container > .se-text > .se-component-content > .se-section > .se-module > p'
    ) # 게시글 내용 찾기.
    payload["title"] = soup.find("title").text
    for title in tags: # 가공
        if '\u200b' in title.text:
            payload["contents"]+=(removeZeroSpace(title.text + '\n'))
        else:
            payload["contents"]+=(removeTag(title.text + '\n'))

    # print(json.dumps(payload))
    print(payload)


try:
    getBlogContent(getFristBlog(keyword))
except IndexError:
    print("\n[ERROR] Keyword : " + keyword + "\n")
print("time :", time.time() - start)
