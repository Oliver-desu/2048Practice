# gui_pyqt6.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QGridLayout, QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from game2048 import Game2048  # 你的核心逻辑

CELL_COLORS = {
    -1: ("#1a1a18", "#ff4444"),  # 最深色，红色字体，显示X
    0: ("#cdc1b4", "#776e65"),
    2: ("#eee4da", "#776e65"),
    4: ("#ede0c8", "#776e65"),
    8: ("#f2b179", "#f9f6f2"),
    16: ("#f59563", "#f9f6f2"),
    32: ("#f67c5f", "#f9f6f2"),
    64: ("#f65e3b", "#f9f6f2"),
    128: ("#edcf72", "#f9f6f2"),
    256: ("#edcc61", "#f9f6f2"),
    512: ("#edc850", "#f9f6f2"),
    1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2"),
    4096: ("#eee4da", "#333333"),
    8192: ("#eedcbd", "#333333"),
    16384: ("#f2f2f2", "#333333"),
    32768: ("#d7ccc8", "#333333"),
    65536: ("#bcaaa4", "#333333"),
}


class Game2048GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2048 with PyQt6")
        self.game = Game2048()

        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)

        # 分数标签
        self.score_label = QLabel("分数: 0")
        score_font = QFont("Arial", 20, QFont.Weight.Bold)
        self.score_label.setFont(score_font)
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.v_layout.addWidget(self.score_label)

        # 棋盘布局
        self.grid = QGridLayout()
        self.v_layout.addLayout(self.grid)

        self.cells = [[QLabel() for _ in range(4)] for _ in range(4)]
        font = QFont("Arial", 24, QFont.Weight.Bold)
        for r in range(4):
            for c in range(4):
                label = self.cells[r][c]
                label.setFixedSize(100, 100)
                label.setFont(font)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                bg, fg = CELL_COLORS[0]
                label.setStyleSheet(f"background-color: {bg}; color: {fg}; border-radius: 10px;")
                self.grid.addWidget(label, r, c)

        self.update_board()

    def update_board(self):
        for r in range(4):
            for c in range(4):
                val = self.game.board[r][c]
                bg_color, fg_color = CELL_COLORS.get(val, ("#3c3a32", "#f9f6f2"))
                label = self.cells[r][c]
                if val == -1:
                    label.setText("X")
                else:
                    label.setText(str(val) if val != 0 else "")
                label.setStyleSheet(f"background-color: {bg_color}; color: {fg_color}; border-radius: 10px;")

        self.score_label.setText(f"分数: {self.game.score if hasattr(self.game, 'score') else 0}")

    def keyPressEvent(self, event):
        key_map = {
            Qt.Key.Key_Up: "up",
            Qt.Key.Key_Down: "down",
            Qt.Key.Key_Left: "left",
            Qt.Key.Key_Right: "right",
            Qt.Key.Key_W: "up",
            Qt.Key.Key_S: "down",
            Qt.Key.Key_A: "left",
            Qt.Key.Key_D: "right",
        }
        if event.key() in key_map:
            moved = self.game.move(key_map[event.key()])
            if moved:
                self.update_board()
                if not self.game.can_move():
                    self.game_over()

    def game_over(self):
        msg = QMessageBox()
        msg.setWindowTitle("Game Over")
        msg.setText("游戏结束！没有可用的移动了。")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
        # 这里可以选择重置游戏
        self.game = Game2048()
        self.update_board()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = Game2048GUI()
    gui.show()
    sys.exit(app.exec())
