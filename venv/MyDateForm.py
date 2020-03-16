from datetime import datetime

# '%s月%s日'포멧에 맞는 오늘 날짜 리턴
def todayDateTypeJ():
    now = datetime.now()
    return ('%s月%s日' % (now.month, now.day))


def todayDateTypeE():
    now = datetime.now()
    return ('%s%s%s_%s%s%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second))


def simpleTodayDateTypeE():
    now = datetime.now()
    return ('%s年 %s月 %s日' % (now.year, now.month, now.day))

