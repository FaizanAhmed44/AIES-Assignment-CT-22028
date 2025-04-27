import math
import random
import time

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # Initialize a 3x3 board
        self.current_winner = None

    def display_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def get_available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def has_empty_squares(self):
        return ' ' in self.board

    def count_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, position, letter):
        if self.board[position] == ' ':
            self.board[position] = letter
            if self.check_winner(position, letter):
                self.current_winner = letter
            return True
        return False

    def check_winner(self, position, letter):
        row_idx = position // 3
        row = self.board[row_idx*3:(row_idx+1)*3]
        if all([spot == letter for spot in row]):
            return True

        col_idx = position % 3
        column = [self.board[col_idx+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        if position % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        return False

class Player:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass

class RandomComputerPlayer(Player):
    def get_move(self, game):
        move = random.choice(game.get_available_moves())
        return move

class HumanPlayer(Player):
    def get_move(self, game):
        valid_move = False
        selected = None
        while not valid_move:
            move = input(self.letter + '\'s turn. Choose a move (0-8): ')
            try:
                selected = int(move)
                if selected not in game.get_available_moves():
                    raise ValueError
                valid_move = True
            except ValueError:
                print('Invalid input. Please try again.')
        return selected

class GeniusComputerPlayer(Player):
    def __init__(self, letter, use_alpha_beta=False):
        super().__init__(letter)
        self.use_alpha_beta = use_alpha_beta

    def get_move(self, game):
        if len(game.get_available_moves()) == 9:
            move = random.choice(game.get_available_moves())
        else:
            if self.use_alpha_beta:
                _, move = self.minimax_alpha_beta(game, self.letter)
            else:
                _, move = self.minimax(game, self.letter)
        return move

    def minimax(self, board_state, player):
        max_player = self.letter
        opponent = 'O' if player == 'X' else 'X'

        if board_state.current_winner == opponent:
            return {'X': -1, 'O': 1}[opponent], None
        elif not board_state.has_empty_squares():
            return 0, None

        if player == max_player:
            best = (-math.inf, None)
        else:
            best = (math.inf, None)

        for move in board_state.get_available_moves():
            board_state.make_move(move, player)
            sim_score, _ = self.minimax(board_state, opponent)
            board_state.board[move] = ' '
            board_state.current_winner = None

            if player == max_player:
                if sim_score > best[0]:
                    best = (sim_score, move)
            else:
                if sim_score < best[0]:
                    best = (sim_score, move)

        return best

    def minimax_alpha_beta(self, board_state, player, alpha=-math.inf, beta=math.inf):
        max_player = self.letter
        opponent = 'O' if player == 'X' else 'X'

        if board_state.current_winner == opponent:
            return {'X': -1, 'O': 1}[opponent], None
        elif not board_state.has_empty_squares():
            return 0, None

        if player == max_player:
            best = (-math.inf, None)
        else:
            best = (math.inf, None)

        for move in board_state.get_available_moves():
            board_state.make_move(move, player)
            sim_score, _ = self.minimax_alpha_beta(board_state, opponent, alpha, beta)
            board_state.board[move] = ' '
            board_state.current_winner = None

            if player == max_player:
                if sim_score > best[0]:
                    best = (sim_score, move)
                alpha = max(alpha, sim_score)
            else:
                if sim_score < best[0]:
                    best = (sim_score, move)
                beta = min(beta, sim_score)

            if beta <= alpha:
                break

        return best

def play(game, x_player, o_player, display_game=True):
    if display_game:
        game.display_board()

    current_letter = 'X'
    while game.has_empty_squares():
        if current_letter == 'O':
            move = o_player.get_move(game)
        else:
            move = x_player.get_move(game)

        if game.make_move(move, current_letter):
            if display_game:
                print(f'{current_letter} makes a move to square {move}')
                game.display_board()
                print('')

            if game.current_winner:
                if display_game:
                    print(f'{current_letter} wins!')
                return current_letter

            current_letter = 'O' if current_letter == 'X' else 'X'

        time.sleep(0.5)

    if display_game:
        print('It\'s a draw!')

def compare_performance():
    game_minimax = TicTacToe()
    game_alpha_beta = TicTacToe()

    x_player_minimax = GeniusComputerPlayer('X', use_alpha_beta=False)
    o_player_random1 = RandomComputerPlayer('O')

    x_player_alpha_beta = GeniusComputerPlayer('X', use_alpha_beta=True)
    o_player_random2 = RandomComputerPlayer('O')

    start_time_minimax = time.time()
    play(game_minimax, x_player_minimax, o_player_random1, display_game=False)
    end_time_minimax = time.time()

    start_time_alpha_beta = time.time()
    play(game_alpha_beta, x_player_alpha_beta, o_player_random2, display_game=False)
    end_time_alpha_beta = time.time()

    print(f"Minimax Execution Time: {end_time_minimax - start_time_minimax:.4f} seconds")
    print(f"Alpha-Beta Execution Time: {end_time_alpha_beta - start_time_alpha_beta:.4f} seconds")

if __name__ == '__main__':
    compare_performance()

    x_player = HumanPlayer('X')
    o_player = GeniusComputerPlayer('O', use_alpha_beta=True)
    tictactoe_game = TicTacToe()
    play(tictactoe_game, x_player, o_player)
