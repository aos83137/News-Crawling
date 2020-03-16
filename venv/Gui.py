import tkinter as tk
from tkinter.messagebox import *
import MainCrawling as mc
import GetData as gd
import pickle
from keywordModel import *


TITLE_FONT = ("Helvetica", 24, "bold")
BUTTON_FONT_1 = ("Helvetica", 16, "bold")
BUTTON_FONT_2 = ("Helvetica", 14)

class ScrawlingApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('News Scrawling')
        self.geometry("1200x960")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        frameTuple = (StartPage, Setting, SearchSetting, NewsPage, ViewNews)

        for F in frameTuple:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="news")

        # self.show_frame("StartPage")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        keywords = get_keyword_list()

        def getdata():
            keyword_list = get_keyword_list()
            str = []
            for i, keyword in enumerate(keyword_list):
                print(keyword["keyword"])
                cm = mc.MainCrawling(keyword["keyword"])

        tk.Frame.__init__(self, parent)
        self.controller = controller


        create_keyword_table()

        label = tk.Label(self, text="News Scrawling", font=TITLE_FONT)
        settingButton = tk.Button(self, text="설정",
                                  command=lambda: controller.show_frame("Setting"))
        newsButton = tk.Button(self, text="뉴스 확인",
                               width=20, height=2, font=BUTTON_FONT_1,
                               command=lambda: controller.show_frame("NewsPage"))
        getDataButton = tk.Button(self, text="즉시 크롤링", width=20, height=2 , font=BUTTON_FONT_1,
                                command=getdata)
        settingButton.pack(anchor='ne', padx=30, pady=30)
        label.pack(fill="x", pady=120)
        newsButton.pack(pady=100)
        getDataButton.pack()






class Setting(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="설정", font=TITLE_FONT)
        # timeButton = tk.Button(self, text="시간대 확인", width=25, height=3, font=BUTTON_FONT_2,
        #                        command=lambda: controller.show_frame("TimeSetting"))
        searchButton = tk.Button(self, text="검색어 확인", width=25, height=3, font=BUTTON_FONT_2,
                                 command=lambda: controller.show_frame("SearchSetting"))
        checkButton = tk.Button(self, text="홈으로", font=BUTTON_FONT_1, width=15, height=2,
                                command=lambda: controller.show_frame("StartPage"))

        label.pack(fill="x", pady=150)
        searchButton.pack(pady=30)
        checkButton.pack(pady=80)


class SearchSetting(tk.Frame):
    def __init__(self, parent, controller):
        # create_keyword_table()
        # drop_keyword_table()
        def addButton(event):
            keyword = entry.get().strip()
            print(keyword)
            if not keyword:
                showerror("오류", "제목 또는 내용을 입력해 주세요")
                return
            add_keyword(keyword)
            refresh()

        def removeButton(event):
            sel = listbox.curselection()
            if not sel:
                showerror("오류", "리스트를 먼저 선택해 주세요")
                return
            _id = ROW_IDS[sel[0]]
            if askyesno("확인", "정말로 삭제하시겠습니까?"):
                remove_keyword(_id)
                refresh()

        def refresh():
            ROW_IDS.clear()
            entry.delete(0, tk.END)  # clear subject
            load_keyword_list()

        def load_keyword_list():
            listbox.delete(0, tk.END)
            keyword_list = get_keyword_list()

            for i, keyword in enumerate(keyword_list):
                ROW_IDS.append(keyword["id"])
                listbox.insert(i, '%s' % (
                    keyword["keyword"]))

        def get_keyword(event):
            _id = ROW_IDS[listbox.curselection()[0]]
            keyword = read_keyword(_id)
            entry.delete(0)


        tk.Frame.__init__(self, parent)
        self.controller = controller

        ROW_IDS = []

        #text생성
        entry = tk.Entry(self,font=TITLE_FONT)
        #라벨생성
        label = tk.Label(self, text="검색어 설정", font=TITLE_FONT)

        #listbox
        fram1 = tk.Frame(self, relief="solid", bd=1)
        scrollbar = tk.Scrollbar(fram1)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(fram1, yscrollcommand  = scrollbar.set , width=30, height=10)
        listbox.bind('<<ListboxSelect>>', get_keyword)

        backButton = tk.Button(self, text="뒤로", font=BUTTON_FONT_1, width=3, height=2,
                                command=lambda: controller.show_frame("Setting"))

        btn_fram = tk.Frame(self)
        add_button = tk.Button(btn_fram, text="저장", font=BUTTON_FONT_1, width=15, height=2,)
        add_button.bind('<Button-1>', addButton)
        delete_button = tk.Button(btn_fram, text="삭제", font=BUTTON_FONT_1, width=15, height=2,)
        delete_button.bind('<Button-1>', removeButton)

        add_button.grid(row=0, column=0)
        delete_button.grid(row=0, column=1)

        load_keyword_list()
        listbox.pack()

        backButton.pack()
        label.pack(fill="x", pady=150)
        fram1.pack()
        entry.pack()
        btn_fram.pack(pady=30)

class NewsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


        def load_news_list():
            listbox.delete(0, tk.END)

            for i in range(len(titles)):
                ROW_IDS.append(len(titles)-i-1)
                listbox.insert(tk.END, "{:>5s}  |  {:>5s}  |   {:<s}   | {:<5s} || {:<5s}".format(str(i+1), days[len(titles)-i-1], keywords [len(titles)-i-1], titles[len(titles)-i-1], medias[len(titles)-i-1]))

        def get_content(event):
            clearContent()
            _id = ROW_IDS[listbox.curselection()[0]]
            # clearContent()

            content.insert(1.0,contents[_id])
            content.pack()

            contentFrame.pack()

        def clearContent():
            content.delete(1.0,tk.END)
            content.pack_forget()

        tk.Frame.__init__(self, parent)
        self.controller = controller

        ROW_IDS = []



        #데이터 가져오기
        titles, contents, medias, keywords, days = gd.GetData.getData(self)

        label = tk.Label(self, text="News", font=TITLE_FONT)
        checkButton = tk.Button(self, text="홈", font=BUTTON_FONT_1, width=15, height=2,
                                command=lambda: controller.show_frame("StartPage"))

        fram2 = tk.Frame(self, relief="solid",bd=1)
        #lsitbox
        fram1 = tk.Frame(fram2, relief="solid", bd=1)
        contentFrame = tk.Frame(fram2)
        content = tk.Text(contentFrame, spacing2=4, width=60, font=BUTTON_FONT_2)

        scrollbar = tk.Scrollbar(fram1)
        scrollbar.pack(side="right", fill="y")
        listbox = tk.Listbox(fram1, yscrollcommand  = scrollbar.set , width=150, height=8)
        listbox.bind('<<ListboxSelect>>', get_content)
        listbox.pack()

        load_news_list()

        fram1.pack()
        content.pack()


        label.pack(fill="x")
        fram2.pack()
        checkButton.pack()



class ViewNews(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


if __name__ == "__main__":
    app = ScrawlingApp()
    app.mainloop()
