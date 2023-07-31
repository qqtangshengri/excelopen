import sys,os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QCompleter
from PyQt5.QtCore import Qt  # 导入Qt枚举类型
import subprocess
import threading
import pystray
from PIL import Image
import keyboard

all_filenames = []
target_directory = r"D:\unitycode1\Config"


class SearchBox(QWidget):
    window_visible = False  # 初始时窗口不可见
    def __init__(self):
        super().__init__()

        self.create_systray_icon()
        # self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("请输入表名部分文字")
        self.search_box.setFixedWidth(1000)
        # completer = QCompleter(["apple", "banana", "orange", "grape", "pineapple", "peach", "pear", "watermelon"])
        filenames = get_all_filenames(target_directory)

        completer = QCompleter(filenames)
        completer.setFilterMode(Qt.MatchContains)  # 设置匹配模式为连续字符匹配
        self.search_box.setCompleter(completer)

        self.search_box.returnPressed.connect(self.on_search)

        self.layout.addWidget(self.search_box)

        self.setLayout(self.layout)
        self.setWindowTitle("快速查找excel")

    def show_window(self):
        self.show()
    def quit_window(self):
        self.icon.stop()

    def windowshowtype(self):
        print
        if self.window_visible:
            self.hide()
            self.window_visible = False
        else:
            self.show()
            self.window_visible = True

    def on_search(self):
        search_query = self.search_box.text()
        print("Search query:", search_query)
        Run_File(target_directory +"\\"+ search_query)
    def create_systray_icon(self):
        """
        使用 Pystray 创建系统托盘图标
        """
        menu = (
            pystray.MenuItem('显示', self.show_window, default=True),
            pystray.Menu.SEPARATOR,  # 在系统托盘菜单中添加分隔线
            pystray.MenuItem('退出', self.quit_window))
        image = Image.open("1.png")
        self.icon = pystray.Icon("icon", image, "图标名称", menu)
        threading.Thread(target=self.icon.run, daemon=True).start()
    def closeEvent(self, event):
        event.ignore()  # 忽略关闭事件
        self.hide()     # 隐藏窗口


def Run_File(directory_path):
    command = f"{directory_path}"
    subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    

def get_all_filenames(directory_path):
    all_filenames = []
    for root, _, filenames in os.walk(directory_path):
        for filename in filenames:
            if "xlsx" in filename:
                # full_path = os.path.join(root, filename)
                all_filenames.append(filename)
    return all_filenames

if __name__ == "__main__": # 添加菜单和图标
    app = QApplication(sys.argv)
    window=SearchBox()
    window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
    window.setWindowFlags(window.windowFlags() & ~int(0x00000008))
    # window.closeEvent = Reghotkey
    window.show()
    window.activateWindow()
    # 创建快捷键
    keyboard.add_hotkey('alt+n', window.windowshowtype)
    sys.exit(app.exec_())  # 程序入口点，进入Qt的事件循环