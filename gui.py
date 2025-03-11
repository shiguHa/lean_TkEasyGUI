import TkEasyGUI as eg
import tkinter as tk

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

        common_font = ("Arial", 12)

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
            font=common_font,
        )
        self.textBox = [eg.Input("input1", key="-input1-", enable_events=True, color="red", font=common_font)]

        tab1_layout = [
            [self.tbl, self.textBox[0]],
            [eg.Button("Update", expand_x=True, font=common_font), eg.Button("Close", font=common_font)]
        ]

        tab2_layout = [
            [eg.Text("This is Tab 2", font=common_font)],
            [eg.Button("Close", font=common_font)],
            [eg.Button("Disable Tab 1", key="-DISABLE_TAB1-", font=common_font)],
            [eg.Button("Enable Tab 1", key="-ENABLE_TAB1-", font=common_font)]
        ]

        self.layout = [[eg.TabGroup([[eg.Tab("あああ1", tab1_layout, key="-TAB1-"), eg.Tab("[Preset]最適化パラメーター", tab2_layout, key="-TAB2-")]], font=common_font)]]
        # create window
        self.win = eg.Window("Table test", self.layout, font=common_font, resizable=True, size=(800, 600))


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
                self.add_textbox()
            if event == "-DISABLE_TAB1-":
                self.set_tab_state("-TAB1-", "disabled")
            if event == "-ENABLE_TAB1-":
                self.set_tab_state("-TAB1-", "normal")

        self.win.close()

    def add_textbox(self):
        new_textbox = eg.Input("", key=f"-input{len(self.textBox) + 1}-", enable_events=True, color="red", font=("Arial", 12))
        self.textBox.append(new_textbox)
        self.win.close()
        tab1_layout = [
            [self.tbl, self.textBox[0]],
            [eg.Button("Update", expand_x=True, font=("Arial", 12)), eg.Button("Close", font=("Arial", 12))]
        ]
        tab2_layout = [
            [eg.Text("This is Tab 2", font=("Arial", 12))],
            [eg.Button("Close", font=("Arial", 12))],
            [eg.Button("Disable Tab 1", key="-DISABLE_TAB1-", font=("Arial", 12))],
            [eg.Button("Enable Tab 1", key="-ENABLE_TAB1-", font=("Arial", 12))]
        ]
        self.layout = [[eg.TabGroup([[eg.Tab("Tab 1", tab1_layout, key="-TAB1-"), eg.Tab("Tab 2", tab2_layout, key="-TAB2-")]], font=("Arial", 12))]]
        self.win = eg.Window("Table test", self.layout, font=("Arial", 12), resizable=True, size=(800, 600))

        # 上揃えにするための設定
        for element in self.win.element_list():
            if isinstance(element.Widget, tk.Widget):
                element.Widget.pack_configure(anchor='n')

    def set_tab_state(self, tab_key, state):
        def recursive_set_state(widget):
            for element in widget.winfo_children():
                print(type(element))
                if isinstance(element, (tk.Button, tk.Entry)):
                    element.configure(state=state)
                recursive_set_state(element)

        recursive_set_state(self.win[tab_key].Widget)

if __name__ == "__main__":
    app = BayesianOptimizationApp()
    app.run()