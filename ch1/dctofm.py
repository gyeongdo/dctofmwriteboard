from bs4 import BeautifulSoup
import requests
import time
import urllib.request
import os
import datetime
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

isSame = False
isMobile = False
dcUrl = "https://gall.dcinside.com/" #첫번쨰 개념글

'''
-------------------------------------------------------------------
    dc 크롤링 시작
--------------------------------------------------------------------
'''

headers = {'Content-Type': 'application/json; charset=utf-8', "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/74.0.3729.169 Chrome/74.0.3729.169 Safari/537.36"}

driver = requests.get("https://gall.dcinside.com/board/lists?id=leagueoflegends3&exception_mode=recommend", headers=headers)

soup = BeautifulSoup(driver.text, "html.parser")

soup = soup.find_all("tr", class_="ub-content us-post")

soup = soup[0]

soup = soup.find("td", class_="gall_tit ub-word")

# 디씨 롤 갤러리 개념글 첫번째 글 제목
title = soup.find("a").getText()
a_tag = soup.find("a")

dcUrl = dcUrl + a_tag['href']


driver.close()


'''
-------------------------------------------------------------------
    fmkorea 시작
--------------------------------------------------------------------
'''

# 에펨코리아 롤 갤 내가 쓴 글 리스트

driver = requests.get("https://www.fmkorea.com/?vid=&mid=lol&category=&search_keyword=wkrdmst&search_target=nick_name")

soup = BeautifulSoup(driver.text, "html.parser")
soups = soup.find_all("td", class_="title hotdeal_var8")

fmTitle = []

for trList in soups:
    fmtitletmp = trList.find("a").getText().replace(" ", "")
    fmTitle.append(fmtitletmp.replace("\t", ""))


'''
-------------------------------------------------------------------
    비교 시  1. 개념글의 첫번째 글과 내가 쓴 글이랑 비교 하기
--------------------------------------------------------------------
'''

for fmTitles in fmTitle:
    # if fmTitles == title.replace(" ", "").replace("\t", ""):
    if fmTitles == title:
        # 같은 글이 있음
        print('이미 썼던 글')
        print('fmTitles : ', fmTitles)
        print('title : ', title)
        print('title == title : ', fmTitles == title)
        isSame = False
    else:
        # 같은 글이 없음
        print('새로운 글')
        print('fmTitles : ', fmTitles)
        print('title : ', title)
        print('title == title : ', fmTitles == title)
        isSame = True

driver.close()


if isSame:
    '''
    -------------------------------------------------------------------
        1. 게시글이 모바일인지 웹인지
    --------------------------------------------------------------------
    '''

    driver = requests.get(dcUrl, headers=headers)
    soup = BeautifulSoup(driver.text, "html.parser")
    soups = soup.find("em", class_="sp_img icon_write_app")
    title = ""

    print(soups)

    if soups != None:
        # 모바일일 경우
        print('mobile')
        res = requests.get(dcUrl, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        # print(soup)
        title = soup.find("span", class_="title_subject")

        upcoming_events_div = soup.select_one('.writing_view_box')
        mobile_tag_arr = []

        html_tag = []
        img_tag_arr = []

        for link in upcoming_events_div.select('div'):
            if len(link('div')) != 0:
                for link in link('div'):
                    if link('img'):
                        for lin in link('img'):
                            html_tag.append(lin['src'])
                    else:
                        html_tag.append(link)

    else:
        # 웹일 경우
        print('web')

        html = requests.get(dcUrl, headers=headers)
        soup = BeautifulSoup(html.text, "html.parser")

        title = soup.find("span", class_="title_subject")
        soup = soup.find("div", class_="writing_view_box")

        html_tag = []
        img_tag_arr = []
        a_tag = soup.find_all('p')

        # tag 형식으로 넣어야 함 <p> or img
        for x in a_tag:
            elements = x.find_all('img')
            if len(elements) == 1:
                for element in elements:
                    html_tag.append(element.get('src'))
            else:
                html_tag.append(x.get_text())

        for i, x in enumerate(a_tag):
            img_tag = x.findChildren("img", recursive=False)
            if len(img_tag) == 0:
                html_tag[i] = x

    '''
    -------------------------------------------------------------------
    # 공통으로 처리 하는 부분 # fmkorea 접속 시작
    --------------------------------------------------------------------
    '''

    '''
    --------------------------------------------------------------------
        fmkorea 접속 시작
    --------------------------------------------------------------------
    '''
    driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
    driver.get("https://www.fmkorea.com/lol")

    time.sleep(2)

    id = ""
    pw = ""

    print(5)
    driver.find_element_by_name('user_id').send_keys('')
    driver.find_element_by_name('password').send_keys('')

    time.sleep(2)

    driver.find_element_by_xpath('//*[@id="header"]/div/div[2]/form/button').click()

    # 글쓰기 버튼 클릭
    driver.find_element_by_xpath('//*[@id="bd_14339012_0"]/div/div[3]/div[2]/a').click()

    # 게시판 제목
    driver.find_element_by_name('title').send_keys(title.get_text())
    # driver.find_element_by_name('title').send_keys('ㅁㄴㅇㄹ')

    time.sleep(2)
    # 게시판 팝업 닫기
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[3]/div/div[2]/div[3]/div[2]/a[2]').click()

    # html편집기 버튼 누르기
    # driver.find_element_by_xpath('//*[@id="smart_content"]/div[1]/ul[9]/li/span/button').click()


    '''
    --------------------------------------------------------------------
        이미지 등록 시작
    --------------------------------------------------------------------
    '''

    # 글 등록 시작
    # 이미지 다운로드
    outpath = "/Users/veneziar/Downloads/image/"

    if not os.path.isdir(outpath):
        os.makedirs(outpath)

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent',
                          'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/74.0.3729.169 Chrome/74.0.3729.169 Safari/537.36'),
                         ('Content-Type', 'application/json; charset=utf-8'), ('Referer', 'https://gall.dcinside.com/')]
    urllib.request.install_opener(opener)

    now = datetime.datetime.now()

    # 1 이미지를 순서대로 입력하기
    print(6)
    print(html_tag)

    for tag in html_tag:
        if (str(tag).startswith("http")):
            url = str(tag)
            # img 다운로드
            outfile = str(now.strftime('%H%M%S')) + '.png'
            print(outfile)
            urllib.request.urlretrieve(url, outpath + outfile)
            time.sleep(1)

            driver.find_element_by_name('Filedata').send_keys(outpath + outfile)
            time.sleep(4)

            # 본문 삽입 버튼 클릭
            driver.find_element_by_xpath('/ html / body / div[1] / div / div / div / div[3] / div / div[2] / form / div[1] / div / div[2] / div[2] / div[2] / input[4]').click()

        else:
            print('tag_text : ', tag.get_text())
            print('tag : ', tag)

    '''
    --------------------------------------------------------------------
        이미지 등록 끝
    --------------------------------------------------------------------
    '''

    '''
    --------------------------------------------------------------------
        html편집기에 글쓰기 시작ㅍ
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    --------------------------------------------------------------------
    '''

    # 2 입력이 끝나면 바디에서 img태그 긁어오기
    time.sleep(2)

    iframe = driver.find_element_by_xpath('//*[@id="editor_iframe_1"]')
    driver.switch_to.frame(iframe)

    body_tag = driver.find_element_by_css_selector('#___body')
    body = body_tag.find_elements_by_tag_name('img')

    for a in body:
        img_tag_arr.append(a.get_attribute('src'))

    print(img_tag_arr)
    # iframe 되돌리기
    driver.switch_to.default_content()
    # bbb.accept() # 확인 버튼 클릭
    driver.find_element_by_xpath('//*[@id="smart_content"]/div[1]/ul[9]/li/span/button').click()

    # 이미지를 삭제하지 말고 바디 부분을 지워주기
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[3]/div/div[2]/form/div[1]/div/div[1]/div[2]/textarea[2]').clear()


    forIndex = 0

    # html_tag는 태그라서 비교가 안됨 ㅜㅜ
    # def OrderedSet(list):
    #     my_set = set()
    #     res = []
    #     for e in list:
    #         if e not in my_set:
    #             res.append(e)
    #             my_set.add(e)
    #
    #     return res
    #
    # html_tag = OrderedSet(html_tag)

    for i, tag in enumerate(html_tag):
        # 이미지 일 때
        if (str(tag).startswith('http')):
            url = str(tag)
            time.sleep(1)
            driver.find_element_by_css_selector('.input_syntax').send_keys('<br />')
            driver.find_element_by_css_selector('.input_syntax').send_keys('<img src="' + img_tag_arr[forIndex] + '" />')
            forIndex = forIndex + 1
        else:
            # 텍스트 일 때
            time.sleep(1)
            if str(tag.get_text()).startswith('- dc'):
                continue
            if str(tag.get_text()).startswith('롤 이야'):
                continue
            else:
                print('else : ', tag)
                driver.find_element_by_css_selector('.input_syntax').send_keys(str(tag))

    '''
    --------------------------------------------------------------------
        html편집기에 글쓰기 끝
    --------------------------------------------------------------------
    '''
    time.sleep(2000)

else:
    # 같은 글이 있음
    driver.close()