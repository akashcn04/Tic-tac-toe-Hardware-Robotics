class TicTacToe:
    def __init__(self):
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

    def __str__(self):
        return "\n".join([" | ".join(["X" if cell == 'X' else "O" if cell == 'O' else " " for cell in row]) for row in self.board])

    def make_move(self, row, col, player):
        if self.board[row][col] == 0:
            self.board[row][col] = player

    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != 0:
                return True
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != 0:
                return True
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            return True
        return False

    def is_board_full(self):
        return all(cell != 0 for row in self.board for cell in row)

    def get_best_move(self):
        best_score = float('-inf')
        best_move = None
        for i in range(9):
            row, col = i // 3, i % 3
            if self.board[row][col] == 0:
                self.board[row][col] = 'O'
                score = self.minimax(0, False)
                self.board[row][col] = 0
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def minimax(self, depth, is_maximizing):
        if self.check_winner():
            return -1 if is_maximizing else 1
        if self.is_board_full():
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                row, col = i // 3, i % 3
                if self.board[row][col] == 0:
                    self.board[row][col] = 'O'
                    score = self.minimax(depth + 1, False)
                    self.board[row][col] = 0
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                row, col = i // 3, i % 3
                if self.board[row][col] == 0:
                    self.board[row][col] = 'X'
                    score = self.minimax(depth + 1, True)
                    self.board[row][col] = 0
                    best_score = min(score, best_score)
            return best_score