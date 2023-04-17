import datetime

def get_dates(date):

    # Создаем массив дат от текущей даты 15 дней
    dates = [date + datetime.timedelta(days=x) for x in range(15)]

    # Исключаем воскресенья
    dates = [ str(d)[-2:]+'-'+str(d)[5:7] for d in dates if d.weekday() != 6]

    return dates
