import random
from logic import check_winner, make_empty_board
import time
import os
from pprint import pprint

import pandas as pd

def record_winner(text, filename, directory):
  file_path = os.path.join(directory, filename)

  with open(file_path, 'a') as f:
    f.write(text + '\n' + '\n')

def dict_to_csv(data):
    return '\n'.join([f'{key}: {value}' for key, value in data.items()])

game_data = {}

class Board:
    def __init__(self):
        self._board = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

    def get_board(self):
        return self._board
    
    def __getitem__(self, index):
        return self._board[index]

    def make_move(self, row, col, symbol):
        self._board[row][col] = symbol

    def get_cell(self, row, col):
        return self._board[row][col]
    
def get_empty_board():
    """
    row_1 = ['O', 'O', 'O']
    row_2 = ['O', 'O', 'O']
    row_3 = ['O', 'O', 'O']

    board = [row_1, row_2, row_3]
    """
    return [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]

def get_player_input(player_input):
    """
    input:
        row,col
    return:
        row: int -> the index of row
        col: int -> the index of column
    """
    row_col_list = player_input.split(",")  # ["1", "1"]
    row, col = [int(x) for x in row_col_list]  # [1,1]
    return row, col

def print_board(board):
    for row in board:
         print(row)  # print will print the variable in a new line


    
class Player:
    def __init__(self, symbol, is_human=True):
        self.symbol = symbol
        self.is_human = is_human

    def get_move(self, board):
        if self.is_human:
            return self.get_human_move()
        else:
            return self.get_bot_move(board)

    def get_human_move(self):
        player_input = input(f"Player {self.symbol} > ")
        try:
            row, col = get_player_input(player_input)
            return row, col
        except ValueError:
            print("Invalid input, try again")
            return self.get_human_move()

    def get_bot_move(self, board):
        # Simple bot logic: choose a random available square
        empty_squares = [(i, j) for i in range(3) for j in range(3) if board[i][j] is None]
        return random.choice(empty_squares)

class Game:
    def __init__(self, playerX, playerO):
        self._board = Board()
        self._playerX = playerX
        self._playerO = playerO
        self._game_id = time.time()

    def run(self):
        current_player = self._playerX
        winner = None
        game_start_time = time.time()
        
        while winner is None:
            print_board(self._board.get_board())

            row, col = current_player.get_move(self._board)
            
            if self._board[row][col] is not None:
                print(f"{row},{col} already has a mark, please choose another place")
                continue

            self._board.make_move(row, col, current_player.symbol)

            winner = check_winner(self._board.get_board())
            current_player = self.switch_player(current_player)

        print_board(self._board)
        if winner == "draw":
            print("It's a draw!")
        else:
            print(f"Player {winner} wins!")


        game_data = {}
        
        game_data['game_id'] = self._game_id
        if winner == 'X':
            game_data['winner'] = 'Human (Player X)'
        elif winner == 'O':
            game_data['winner'] = 'Bot (Player O)'
        game_data['num_moves'] = self.calculate_total_moves()
        game_data['playerX_symbol'] = self._playerX.symbol
        game_data['playerO_symbol'] = self._playerO.symbol
        # game_data = {
        #     'game_id': self._game_id,
        #     'winner': 'Human (Player X)' if winner == 'X' else 'Bot (Player O)' if winner == 'O' else 'Draw',
        #     'num_moves': self.calculate_total_moves(),
        #     'playerX_symbol': self._playerX.symbol,
        #     'playerO_symbol': self._playerO.symbol
        # }

        # csv_player_data = dict_to_csv(game_data)
        # record_winner(csv_player_data, "database.csv", "logs")

        # pprint(game_data)
        # pd.DataFrame(game_data).to_csv("log/database.csv")

        
        file_path = "logs/database.csv"
        if not os.path.exists(file_path):
            pd.DataFrame([game_data]).to_csv(file_path, index=False)  # Create the file if it doesn't exist
        else:
            pd.DataFrame([game_data]).to_csv(file_path, mode='a', header=False, index=False) 


    def calculate_total_moves(self):
        total_moves = 0
        for row in self._board.get_board():
            for cell in row:
                if cell is not None:
                    total_moves += 1
        return total_moves

    def switch_player(self, current_player):
        return self._playerO if current_player == self._playerX else self._playerX

        game_data = {}
        game_end_time = time.time()
        game_data['game_id'] = self._game_id
        game_data['game_duration'] = game_end_time - game_start_time
        if winner == 'X':
            game_data['winner'] = 'Human (Player X)'
        elif winner == 'O':
            game_data['winner'] = 'Bot (Player O)'
        game_data['num_moves'] = self.calculate_total_moves()
        game_data['playerX_symbol'] = self._playerX.symbol
        game_data['playerO_symbol'] = self._playerO.symbol

        pprint(game_data)
        pd.DataFrame(game_data).to_csv("logs/database.csv")




# main.py



if __name__ == "__main__":
    num_players = int(input("Enter the number of players (1 or 2): "))
    board = get_empty_board()

    if num_players == 1:
        human_symbol = input("Enter your symbol (X or O): ").upper()
        human_player = Player(human_symbol)
        bot_symbol = "X" if human_symbol == "O" else "O"
        bot_player = Player(bot_symbol, is_human=False)

        game = Game(human_player, bot_player)
    elif num_players == 2:
        playerX = Player("X")
        playerO = Player("O")
        game = Game(playerX, playerO)
    else:
        print("Invalid number of players. Exiting.")
        exit()

    game.run()



