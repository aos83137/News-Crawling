import pandas as pd
import glob
import os

class GetData():

    def __init__(self):
        pass

    input_file = r'.\crawlingData\*.csv' # csv파일들이 있는 디렉토리 위치
    output_file = r'.\crawlingData\output.csv' # 병합하고 저장하려는 파일명
    allFile_list = glob.glob(os.path.join(input_file)) # glob함수로 sales_로 시작하는 파일들을 모은다



    #merge
    def merge(self):
        allData = [] # 읽어 들인 csv파일 내용을 저장할 빈 리스트를 하나 만든다
        for file in GetData.allFile_list:
            df = pd.read_csv(file) # for구문으로 csv파일들을 읽어 들인다
            allData.append(df) # 빈 리스트에 읽어 들인 내용을 추가한다

        dataCombine = pd.concat(allData, axis=0, ignore_index=True) # concat함수를 이용해서 리스트의 내용을 병합
        # axis=0은 수직으로 병합함. axis=1은 수평. ignore_index=True는 인데스 값이 기존 순서를 무시하고 순서대로 정렬되도록 한다.
        # dataCombine.to_csv(output_file, index=False) # to_csv함수로 저장한다. 인데스를 빼려면 False로 설정

        dup_result =dataCombine.drop_duplicates('title', keep='last') #병합

        return dup_result

    def getData(self):
        data = GetData.merge(self);

        a_title = []
        a_content = []
        a_media = []
        a_keyword = []
        a_day = []
        for i in range(len(data)):
            for idx, row in enumerate(data.iloc[i]):
                if(idx%5 == 0):
                    a_title.append(row)
                elif(idx%5 == 1):
                    a_content.append(row)
                elif(idx%5 == 2):
                    a_media.append(row)
                elif(idx%5 == 3):
                    a_keyword.append(row)
                elif(idx%5 == 4):
                    a_day.append(row)

        return a_title, a_content, a_media, a_keyword, a_day
