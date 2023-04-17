import datetime

def get_dates(date):

    # Создаем массив дат от текущей даты 15 дней
    dates = [date + datetime.timedelta(days=x) for x in range(15)]

    # Исключаем воскресенья
    dates = [ str(d)[-2:]+'-'+str(d)[5:7] for d in dates if d.weekday() != 6]

    return dates


def get_time_list(start: int = 8, end: int = 18):
    time_list = []
    hour = start
    minute = 0
    while hour < end:
        time_list.append(f"{hour:02d}:{minute:02d}")
        minute += 30
        if minute == 60:
            hour += 1
            minute = 0
    time_list.append("18:00")
    return time_list

print(get_time_list())