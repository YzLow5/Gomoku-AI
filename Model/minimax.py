import random

class TicTacToe: 
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.human_player = "O"
        self.ai_player = "X"
    
    def print_board(self):
        for i in range(0, 9, 3):
            print(f"{self.board[i]} | {self.board[i+1]} | {self.board[i+2]}")
            if i < 6:
                print("-------------")

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == " "]
    
    def make_move(self, position, player):
        if self.board[position] == " ":
            self.board[position] = player
            return True
        return False
    
    def is_board_full(self):
        return " " not in self.board
    
    def check_winner(self):
        # Kiểm tra hàng ngang
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] != " ":
                return self.board[i]
        # Kiểm tra cột dọc    
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != " ":
                return self.board[i]
        # Kiểm tra đường chéo
        if self.board[0] == self.board[4] == self.board[8] != " ":
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != " ":
            return self.board[2]
        return None
    
    def game_over(self):
        return self.check_winner() is not None or self.is_board_full()

    # THÊM HÀM NÀY: Để AI tìm nước đi tốt nhất
    def get_best_move(self):
        best_score = float("-inf")
        move = None
        for m in self.available_moves():
            self.board[m] = self.ai_player
            score = self.minimax(0, False)
            self.board[m] = " "
            if score > best_score:
                best_score = score
                move = m
        return move
    
    def minimax(self, depth, is_maximizing):
        winner = self.check_winner()
        if winner == self.ai_player: return 1
        if winner == self.human_player: return -1
        if self.is_board_full(): return 0
        
        if is_maximizing:
            best_score = float("-inf")
            for move in self.available_moves():
                self.board[move] = self.ai_player
                score = self.minimax(depth + 1, False)
                self.board[move] = " "
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for move in self.available_moves():
                self.board[move] = self.human_player
                score = self.minimax(depth + 1, True)
                self.board[move] = " "
                best_score = min(score, best_score)
            return best_score
    
    def play_game(self):
        print("Welcome to Tic Tac Toe")
        print("Enter positions (0-8) as shown below:")
        print("0 | 1 | 2\n---------\n3 | 4 | 5\n---------\n6 | 7 | 8\n")

        ai_turn = random.choice([True, False])

        while not self.game_over():
            self.print_board()
            if ai_turn:
                print("\nAI's turn...")
                move = self.get_best_move()
                self.make_move(move, self.ai_player)
            else:
                valid_move = False
                while not valid_move:
                    try:
                        move = int(input("\nYour turn (0-8): "))
                        if 0 <= move <= 8 and self.make_move(move, self.human_player):
                            valid_move = True
                        else:
                            print("Invalid move! Try again.")
                    except ValueError:
                        print("Please enter a number between 0 and 8!")
            
            ai_turn = not ai_turn # Đổi lượt (đã sửa vị trí thụt lề)

        self.print_board()
        winner = self.check_winner()
        if winner == self.ai_player:
            print("\nAI wins!")
        elif winner == self.human_player:
            print("\nCongratulations! You win!")
        else:
            print("\nIt's a tie!")

if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()