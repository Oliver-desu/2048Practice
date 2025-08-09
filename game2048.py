import random


class Game2048:
    def __init__(self, size=4, init_board=None):
        self.size = size
        self.score = 0
        if init_board:
            self.board = [row[:] for row in init_board]
        else:
            self.board = [[0] * size for _ in range(size)]
            self.spawn_tile()
            self.spawn_tile()

    def spawn_tile(self):
        """随机在空位置生成 2 或 4"""
        empty_cells = [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] == 0]
        if not empty_cells:
            return
        r, c = random.choice(empty_cells)
        self.board[r][c] = 4 if random.random() < 0.1 else 2  # 10% 生成 4

    def compress(self, row):
        """将一行数字向左压缩（去掉 0 中间的空隙）"""
        new_row = [num for num in row if num != 0]
        new_row += [0] * (self.size - len(new_row))
        return new_row

    def merge(self, row):
        """合并一行相同的数字"""
        for i in range(self.size - 1):
            if row[i] > 0 and row[i] == row[i + 1]:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return row

    def move_left(self):
        moved = False
        new_board = []
        for row in self.board:
            compressed = self.compress(row)
            merged = self.merge(compressed)
            new_row = self.compress(merged)
            new_board.append(new_row)
            if new_row != row:
                moved = True
        self.board = new_board
        return moved

    def move_right(self):
        self.reverse()
        moved = self.move_left()
        self.reverse()
        return moved

    def move_up(self):
        self.transpose()
        moved = self.move_left()
        self.transpose()
        return moved

    def move_down(self):
        self.transpose()
        moved = self.move_right()
        self.transpose()
        return moved

    def reverse(self):
        """水平翻转棋盘"""
        self.board = [row[::-1] for row in self.board]

    def transpose(self):
        """矩阵转置"""
        self.board = [list(row) for row in zip(*self.board)]

    def move(self, direction):
        """执行移动并生成新方块"""
        moves = {
            "left": self.move_left,
            "right": self.move_right,
            "up": self.move_up,
            "down": self.move_down
        }
        if direction in moves:
            moved = moves[direction]()
            if moved:
                self.spawn_tile()
            return moved
        return False

    def can_move(self):
        """判断是否还能移动"""
        # 只要有空格
        if any(0 in row for row in self.board):
            return True
        # 或者有相邻相等的
        for r in range(self.size):
            for c in range(self.size - 1):
                if self.board[r][c] == self.board[r][c + 1]:
                    return True
        for c in range(self.size):
            for r in range(self.size - 1):
                if self.board[r][c] == self.board[r + 1][c]:
                    return True
        return False

    def print_board(self):
        for row in self.board:
            print("\t".join(str(num) if num != 0 else "." for num in row))
        print(f"Score: {self.score}")
        print("-" * 20)


if __name__ == "__main__":
    game = Game2048()
    game.print_board()

    while game.can_move():
        move = input("Move (w/a/s/d): ").strip().lower()
        direction_map = {"w": "up", "a": "left", "s": "down", "d": "right"}
        if move in direction_map:
            if game.move(direction_map[move]):
                game.print_board()
            else:
                print("Can't move that way!")
        else:
            print("Invalid input! Use w/a/s/d.")
    print("Game Over!")
