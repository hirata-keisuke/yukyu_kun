from collections import defaultdict
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import datetime, jpholiday, locale, calendar, random
from itertools import combinations

class App(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        # タイトルとウィンドウサイズ
        self.title('有給休暇 おすすめ君')
        self.geometry('700x300')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ------------------- 有給設定 入力フォーム フレーム --------------------------
        
        # column ____0________1_________2______3______4______5___6__
        # row |                                                     |
        #  0  |   有給休暇 設定入力                                    |
        #  1  | 消化有給数            <フォーム>                       |
        #  2  | 有休取得期間          <フォーム>  ~   <フォーム>         |
        #  3  | オプション  休みの間隔  <フォーム> 日                    |
        #  4  |           独自の休暇  <フォーム> 名称 <フォーム> [+] [-] |
        #  5  |_______________________[決定]_________________________|

        # 入力用フレーム
        self.input_frame = ttk.Frame()
        self.input_frame.grid(column=0, row=0, sticky="nsew")

        self.titleLabel1 = ttk.Label(self.input_frame, text="有給休暇 設定入力", font=('Arial Block', '35'))
        self.titleLabel1.grid(column=0, row=0, columnspan=2)

        # 消化する有給休暇日数について
        self._create_num()

        # 有給休暇を取得する期間について
        self._create_period()

        ttk.Label(self.input_frame, text="オプション").grid(column=0, row=3)

        # 休みと休みの間の日数について
        self._create_span()

        # その他の独自の休暇について
        self.originals_date = list() # 日程用フォーム
        self.originals_name = list() # 名称用フォーム
        self.original_index = 0 # 独自休暇用インデックス
        self.insert_label = tk.Label(
            self.input_frame, text="+", fg="#33ff33", font=('Arial Black', 20)
        )
        self.remove_label = tk.Label(
            self.input_frame, text="-", fg="#ff3333", font=('Arial Black', 20)
        )

        # 決定ボタン
        self.output_button = ttk.Button(
            self.input_frame, text="決定", command=lambda : self._change_page(self.result_frame)
        )
        self._create_original(self.original_index)

        # ------------------- 有給休暇 おすすめフレーム --------------------------
        # 結果用フレーム
        self.result_frame = ttk.Frame()
        self.result_frame.grid(column=0, row=0, sticky="nsew")

        self.titleLabel2 = ttk.Label(
            self.result_frame, text="有給休暇 おすすめ", font=('Arial Block', '35')
        )
        self.titleLabel2.grid(column=0, row=0, columnspan=2)
        
        self.input_frame.tkraise()

    def _create_num(self):
        """
        消化有給日数を入力する領域を作成する
        """
        ttk.Label(self.input_frame, text="消化有給数").grid(column=0, row=1, sticky=tk.W+tk.E)
        self.entry_num = ttk.Entry(self.input_frame, width=3,)
        self.entry_num.grid(column=2, row=1)

    def _create_period(self):
        """
        有給休暇を取得する期間を入力する領域を作成する
        """
        ttk.Label(self.input_frame, text="有給取得期間").grid(column=0, row=2, sticky=tk.W+tk.E)
        # スタート
        self.entry_period_s = DateEntry(
            self.input_frame, showweeknumbers=False, locale="ja_JP", foreground="#000"
        )
        self.entry_period_s.grid(column=2, row=2, sticky=tk.W+tk.E)

        self.label_kara = ttk.Label(self.input_frame, text="〜").grid(column=3, row=2)
        # エンド
        self.entry_period_e = DateEntry(
            self.input_frame, showweeknumbers=False, locale="ja_JP", foreground="#000"
        )
        self.entry_period_e.grid(column=4, row=2)

    def _create_span(self):
        """
        休みと休みの間隔の希望を入力する領域を作成する
        """
        ttk.Label(self.input_frame, text="休みの間隔", anchor=tk.W).grid(column=1, row=3)
        self.entry_span = ttk.Entry(self.input_frame, width=2)
        self.entry_span.insert(0, "10")
        self.entry_span.grid(column=2, row=3)
        ttk.Label(self.input_frame, text="日", anchor=tk.E).grid(column=3, row=3)

    def _create_original(self, original_index):
        """
        独自の休暇を入力する領域を作成する
        """
        ttk.Label(self.input_frame, text="独自の休暇日程:").grid(column=1, row=4)
        ttk.Label(self.input_frame, text="名称:").grid(column=3, row=4)

        # 日程と名称のフォームを追加する
        self.originals_date.insert(original_index, DateEntry(
            self.input_frame, showweeknumbers=False, locale="ja_JP", foreground="#000"
        ))
        self.originals_name.insert(original_index, tk.Entry(self.input_frame))

        self._updateOriginal(original_index)

    def _insertOriginal_click(self, event, id):
        """
        追加用ラベルをクリックした場合に動作する
        """
        self.original_index += 1
        self._create_original(self.original_index)

    def _removeOriginal_click(self, event, id):
        """
        削除用ラベルをクリックした場合に動作する
        """

        if id > 0:
            self.originals_date[id].grid_forget()
            self.originals_name[id].grid_forget()

            self.originals_date.pop()
            self.originals_name.pop()
            
        self.original_index -= 1
        self._updateOriginal(self.original_index)

    def _updateOriginal(self, index):
        """
        追加・削除したものを再配置する
        """
        for i in range(0, index+1):
            self.originals_date[i].grid(column=2, row=4+i)
            self.originals_name[i].grid(column=4, row=4+i)

            if i == index:
                self.insert_label.grid(column=5, row=4+i)
                self.remove_label.grid(column=6, row=4+i)

        # 追加用ラベルにクリックイベントを設定
        self.insert_label.bind(
            '<1>', lambda event, id=self.original_index: self._insertOriginal_click(event, id)
        )

        # 削除用ラベルにクリックイベントを設定
        self.remove_label.bind(
            '<1>', lambda event, id=self.original_index: self._removeOriginal_click(event, id)
        )

        self.output_button.grid(column=2, row=5+i)

    def _change_page(self, frame):
        """
        フレーム切り替え用の関数
        """
        if self.entry_period_s.get_date()>self.entry_period_e.get_date():
            self.input_frame.tkraise()

        else:
            self._calc_yukyu()
            self._create_output()
            frame.tkraise()

    def _calc_yukyu(self):
        """
        入力に基づいて有給休暇を計算する
        """
        start = self.entry_period_s.get_date()
        start = datetime.date(start.year, start.month, 1)
        end = self.entry_period_e.get_date()
        end = datetime.date(end.year, end.month, calendar.monthrange(end.year, end.month)[1])
        if start.year==end.year and start.month == end.month:
            ttk.Label(self.result_frame, text="自分で考えろ", font=('Arial Block', '35'),
                        foreground="#ff3333").grid(column=1, row=1, columnspan=2)
            return 0

        locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
        one_day = datetime.timedelta(days=1)
        rest_or_not = dict()
        rest_month = defaultdict(int)
        the_day = start

        while the_day<=end:
            
            if the_day.strftime("%A") == "土曜日":
                rest_month[the_day.strftime("%Y%m%d")]=1
            
            elif the_day.strftime("%A") == "日曜日":
                rest_month[the_day.strftime("%Y%m%d")]=1
                if jpholiday.is_holiday(the_day): # 振替休日
                    rest_month[(the_day+one_day).strftime("%Y%m%d")]=1
                
            else:
                if rest_month[the_day.strftime("%Y%m%d")]==0:
                    rest_month[the_day.strftime("%Y%m%d")]=0

            if the_day.strftime("%m") != (the_day+one_day).strftime("%m"):
                rest_or_not[the_day.strftime("%Y%m")] = list(rest_month.values())
                rest_month = defaultdict(int)
            the_day += one_day
        
        num_rest = int(self.entry_num.get())
        span = int(self.entry_span.get())
        q, r = divmod(num_rest, len(rest_or_not))
        add_rest = [q+1 if i < r else q for i, _ in enumerate(range(len(rest_or_not)))]

        new_rest = dict()
        for i, rest in enumerate(rest_or_not.items()):

            while True:
                zeros = [index for index, value in enumerate(rest[1]) if value==0]
                candidates = random.sample(zeros, add_rest[i])
                
                _flags = list()
                for a, b in combinations(candidates, 2):
                    _flags.append(abs(a-b)>span)
                if all(_flags):
                    break
            
            new_rest[rest[0]] = sorted(candidates)
        
        self.new_rest = new_rest

    def _create_output(self):
        for i, ym in enumerate(self.new_rest.keys()):
            for j, d in enumerate(self.new_rest[ym]):
                ttk.Label(
                    self.result_frame, text=ym[:4]+"/"+ym[4:]+"/"+"{:d}".format(d+1), font=('Arial Block', '35')
                ).grid(column=1+j, row=2+i)


if __name__ == "__main__":

    app = App()
    app.mainloop()