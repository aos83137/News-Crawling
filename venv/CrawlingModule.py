from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
from pathlib import Path
import MyDateForm
import CheckingDate
import GetNewContents

class md:
    # 뉴스의 날짜와 오늘날짜의 확인
    def __init__(self, keyword):
        self.keyword = keyword
    def runCrawling(self):
        page = 1
        news_links = []
        todayNewsCnt = 0
        newsContents = []
        searchKey = self.keyword
        def pageCnt():
            page = 1
            todayNewsCnt = 0
            news_links = []

            while True:
                # 검색 사이트
                url = "https://news.yahoo.co.jp/search/;_ylt=A2Rivc6iSMZdWQ4A0xeEmuZ7?p="+searchKey+"&vaop=a&to=0&st=&c_=dom&c_=c_int&c_=bus&c_=c_ent&c_=c_sci&c_=c_life&c_=loc&ei=UTF-8&&b=" + str(
                    page)

                # url 요청해서 응답 받아서 저장
                response = requests.get(url)
                # 응답받은 text 을 html변수에 저장
                html = response.text
                # 키워드로 검색한 내용 링크 리스트 저장용 변수 선언
                # bs4사용
                soup = BeautifulSoup(html, 'html.parser')

                getNewsCount = soup.select('.l > .txt > p > .d')

                # href를 찾는 코드
                goToATages = soup.select('h2.t > a')
                if len(goToATages) != 0:
                    for atag in range(len(goToATages)):
                        newsDate=0
                        news_links.append(goToATages[atag]['href'])
                        newsDate = soup.select('.l > .txt > p > .d')[atag].text.split('（')[0]  # 월月일日추출
                        if CheckingDate.todayNews(newsDate):
                            todayNewsCnt += CheckingDate.todayNews(newsDate)
                        else:
                            return todayNewsCnt

                else:
                    return todayNewsCnt

                page += 10
                print(page)
        count = pageCnt()
        print('count : ', count)
        lastPageNum = count
        while page <= lastPageNum:
            # 검색 사이트
            url = "https://news.yahoo.co.jp/search/;_ylt=A2Rivc6iSMZdWQ4A0xeEmuZ7?p=" + searchKey + "&vaop=a&to=0&st=&c_=dom&c_=c_int&c_=bus&c_=c_ent&c_=c_sci&c_=c_life&c_=loc&ei=UTF-8&&b=" + str(
                page)

            # url 요청해서 응답 받아서 저장
            response = requests.get(url)
            # 응답받은 text 을 html변수에 저장
            html = response.text
            # 키워드로 검색한 내용 링크 리스트 저장용 변수 선언

            # bs4사용
            soup = BeautifulSoup(html, 'html.parser')

            getNewsCount = soup.select('.l > .txt > p > .d')

            # href를 찾는 코드
            goToATages = soup.select('h2.t > a')
            for atag in range(len(goToATages)):
                news_links.append(goToATages[atag]['href'])
                newsDate = soup.select('.l > .txt > p > .d')[atag].text.split('（')[0]  # 월月일日추출
                if CheckingDate.todayNews(newsDate):
                    todayNewsCnt += CheckingDate.todayNews(newsDate)
                else:
                    break

                newsContents.append(GetNewContents.GetNewContents(news_links[atag + page - 1],self.keyword))
                print(todayNewsCnt)

            ###이부분 해결하자
            # getNewsCount(news_links)
            page += 10
        # print(newsContents)
        table = pd.DataFrame(newsContents, columns=['title', 'content', 'media','keyword', 'date'])
        table.head()
        table.drop_duplicates(inplace=True)  # 중복행 제거

        # 폴더 생성
        dir_folder = Path('./crawlingData')
        print(str(dir_folder))
        if not dir_folder.exists():
            dir_folder.mkdir(parents=True)
        table.to_csv('./' + str(dir_folder) + '/'+self.keyword+'_'+ MyDateForm.todayDateTypeE()+'.csv', index=False ,encoding="utf-8-sig")

