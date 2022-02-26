import numpy as np
import datetime
import matplotlib.pyplot as plt

from get_holiday import get_holiday, date_range

def gaussian_kernel(size=2, sigma2=1):
    """
    ガウシアンカーネル。休日の影響を計算する日を中心としたガウシアンを計算する。

    Parameters
    ==========
    size : int
        カーネルのサイズ。
    sigma2 : float
        ガウシアンの分散。

    Returns
    =======
    filter : ndarray
        フィルターの値を持つnumpy配列。サイズはsize+1+size。
    """

    _grid = np.arange(-size, size+1)

    #return 1/np.sqrt(2*np.pi*sigma2) * np.exp(-_grid**2/(2*sigma2))
    return np.exp(-_grid**2/(2*sigma2))

    ...

if __name__ == "__main__":

    start = "20220401"
    end = "20230331"
    
    holidays = get_holiday(start, end)

    start = datetime.datetime.strptime(start, "%Y%m%d")
    start = datetime.date(start.year, start.month, start.day)
    end = datetime.datetime.strptime(end, "%Y%m%d")
    end = datetime.date(end.year, end.month, end.day)
    dates = [date.strftime("%Y%m%d") for date in date_range(start,end)]
    bars = [1 if d in holidays else 0 for d in dates]

    size=2
    filter = gaussian_kernel(size=size, sigma2=0.5)
    print(filter)
    _bars = np.concatenate([np.zeros(size), bars, np.zeros(size)])
    filtered = np.zeros_like(bars, dtype=np.float64)

    for i in range(len(filtered)):
        _target = _bars[i+size-size:i+size+size+1]
        filtered[i] = filter @ _target
        
    plt.plot(np.arange(len(bars)), bars)
    plt.plot(np.arange(len(filtered)), filtered)
    plt.plot(np.arange(len(filtered)), np.max(filtered)-filtered)
    plt.grid()
    plt.show()