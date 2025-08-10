import sys
import subprocess
from PyQt6.QtWidgets import QApplication
from gui_pyqt6 import Game2048GUI


def run_game():
    app = QApplication(sys.argv)
    game = Game2048GUI()
    game.show()
    sys.exit(app.exec())


def build_exe():
    # 调用 pyinstaller 生成单文件可执行程序
    cmd = [
        "pyinstaller",
        "--onefile",
        "--noconsole",    # 不显示终端窗口
        "gui_pyqt6.py"
    ]
    subprocess.run(cmd)


if __name__ == "__main__":
    build_exe()
    run_game()
