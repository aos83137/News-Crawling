import requests
from bs4 import BeautifulSoup
import MyDateForm

def getNewContents(news_link,keyword):
    print(news_link)
    response2 = requests.get(news_link)
    html2 = response2.text
    soup2 = BeautifulSoup(html2, 'html.parser')
    content = ''
    try:
        mediaNullCheck = soup2.select_one('p.ynCobrandBanner > a> img')['alt']
    except:
        mediaNullCheck=0
        print('예외 : 미디어가 없는 기사입니다.');
    if(not soup2.select_one('.hd > h1')):
        title = 'none title'
    else:
        title = soup2.select_one('.hd > h1').text
    try:
        if(soup2.select_one('p.ynDetailText')):
            content = soup2.select_one('p.ynDetailText').text
        elif(soup2.select_one('.yjDirectSLinkTarget')):
            content = soup2.select_one('.yjDirectSLinkTarget').text
        elif(soup2.select_one('#ual')):
            print('check')
            contents = soup2.find_all('#ual>p')
            for piece in contents:
                print(type(piece))
                print(piece)
                print(piece.text)
                content = content +'\n'+ piece.text
        else:
            content=0

    except:
        print(e)

    # media가 없을 경우를 위한 3항 연산
    media = mediaNullCheck if mediaNullCheck else "None media"

    print(title)

    return title, content, media, keyword, MyDateForm.simpleTodayDateTypeE()
