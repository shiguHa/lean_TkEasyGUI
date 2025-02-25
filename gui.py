import TkEasyGUI as eg

class BayesianOptimizationApp:
    def __init__(self):
        self.create_widgets()

    def create_widgets(self):
        self.data = []
        for row in range(100):
            rows = []
            for col in range(30):
                rows.append(f"@{row:03}x{col:03}")
            self.data.append(rows)

        self.tbl = eg.Table(
            key="-table-",
            values=self.data[1:],  # テーブルに表示するデータ(ヘッダ行を含まない)を指定
            headings=self.data[0],  # ヘッダ行を指定
            expand_x=True,  # ウィンドウのX方向にサイズを合わせる
            expand_y=True,  # ウィンドウのY方向にサイズを合わせる
            justification="center",  # セルを中央揃えにする
            auto_size_columns=False,  # 自動的にカラムを大きくする
            max_col_width=30,  # 最大カラムサイズを指定
            enable_events=True,  # イベントを有効にする
            vertical_scroll_only=False,  # 垂直スクロールバーを表示する
            font=("Arial", 12),
        )
        textBox = [eg.Input("input1", key="-input1-", enable_events=True, color="red")]

        layout = [[self.tbl], [eg.Button("Update", expand_x=True), eg.Button("Close")], textBox]
        # create window
        self.win = eg.Window("Table test", layout, font=("Arial", 12), resizable=True, size=(800, 600))

    def run(self):
        while True:
            event, values = self.win.read()
            print("@@@", event, values)
            if event == eg.WIN_CLOSED:
                break
            if event == "Close":
                break
            if event == "Update":
                print("Update")

        self.win.close()