import datetime, jpholiday
import numpy as np
import matplotlib.pyplot as plt

def get_holiday(start, end):
    """
    期間内の休日を返す
    
    Parameters
    ==========
    start : str
        期間の開始日を表す文字列。yyyymmdd形式を指定する。
    end : str
        期間の終了日を表す文字列。yyyymmdd形式を指定する。

    Return
    ======
    holiday_flags : list
        期間の休日を表す文字列のリスト。日付はyyyymmdd形式を指定する。    
    """    
    # 開始日の変換
    start = datetime.datetime.strptime(start, "%Y%m%d")
    start = datetime.date(start.year, start.month, start.day)
    
    # 終了日の変換
    end = datetime.datetime.strptime(end, "%Y%m%d")
    end = datetime.date(end.year, end.month, end.day)

    # 休祝日のみをリストに格納する
    holidays = list()
    for date in date_range(start, end):
        if date.weekday() >= 5 or jpholiday.is_holiday(date):
            holidays.append(date.strftime("%Y%m%d"))
        elif date.weekday() == 6 and jpholiday.is_holiday(date):
            holidays.append((date+datetime.timedelta(1)).strftime("%Y%m%d"))

    return holidays

def date_range(start, stop, step=datetime.timedelta(days=1)):
    """
    日付のイテレーションを回すジェネレータを生成する

    Parameters
    ==========
    start : date型
        期間の開始日を表すdate型。
    stop : date型
        期間の終了日を表すdate型。
    step : timedelta型
        イテレーションの感覚を表すtimedelta型

    """
    current = start
    while current <= stop:
        yield current
        current += step

if __name__ == "__main__":
    start = "20220401"
    end = "20230331"
    holidays = get_holiday(start=start, end=end)

    start = datetime.datetime.strptime(start, "%Y%m%d")
    start = datetime.date(start.year, start.month, start.day)
    end = datetime.datetime.strptime(end, "%Y%m%d")
    end = datetime.date(end.year, end.month, end.day)
    dates = [date.strftime("%Y%m%d") for date in date_range(start,end)]
    
    x = np.arange(len(dates))
    bars = [1 if d in holidays else 0 for d in dates]

    plt.bar(x, bars)
    plt.xticks(np.arange(len(x), 10))
    plt.xticks(
        np.arange(0, len(x), 10), [dates[i] for i in range(len(dates)) if i%10==0], 
        rotation=30
    )
    plt.grid()
    plt.show()