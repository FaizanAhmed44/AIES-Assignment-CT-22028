import math
import random
import time

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # 3x3 board
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([s == letter for s in row]):
            return True

        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([s == letter for s in column]):
            return True

        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([s == letter for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == letter for s in diagonal2]):
                return True

        return False

class Player:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass

class RandomComputerPlayer(Player):
    def get_move(self, game):
        square = random.choice(game.available_moves())
        return square

class HumanPlayer(Player):
    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8): ')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid move. Try again.')
        return val

class GeniusComputerPlayer(Player):
    def __init__(self, letter, use_alpha_beta=False):
        super().__init__(letter)
        self.use_alpha_beta = use_alpha_beta

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())  # pick randomly
        else:
            if self.use_alpha_beta:
                _, square = self.minimax_alpha_beta(game, self.letter)
            else:
                _, square = self.minimax(game, self.letter)
        return square

    def minimax(self, state, player):
        max_player = self.letter  # yourself
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {'X': -1, 'O': 1}[other_player], None
        elif not state.empty_squares():
            return 0, None

        if player == max_player:
            best = (-math.inf, None)  # (score, move)
        else:
            best = (math.inf, None)

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score, _ = self.minimax(state, other_player)
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score = sim_score

            if player == max_player:
                if sim_score > best[0]:
                    best = (sim_score, possible_move)
            else:
                if sim_score < best[0]:
                    best = (sim_score, possible_move)

        return best

    def minimax_alpha_beta(self, state, player, alpha=-math.inf, beta=math.inf):
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {'X': -1, 'O': 1}[other_player], None
        elif not state.empty_squares():
            return 0, None

        if player == max_player:
            best = (-math.inf, None)
        else:
            best = (math.inf, None)

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score, _ = self.minimax_alpha_beta(state, other_player, alpha, beta)
            state.board[possible_move] = ' '
            state.current_winner = None

            if player == max_player:
                if sim_score > best[0]:
                    best = (sim_score, possible_move)
                alpha = max(alpha, sim_score)
            else:
                if sim_score < best[0]:
                    best = (sim_score, possible_move)
                beta = min(beta, sim_score)

            if beta <= alpha:
                break

        return best

def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board()

    letter = 'X'
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, letter):
            if print_game:
                print(letter + f' makes a move to square {square}')
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    print(letter + ' wins!')
                return letter

            letter = 'O' if letter == 'X' else 'X'

        time.sleep(0.5)

    if print_game:
        print('It\'s a tie!')

def compare_performance():
    game1 = TicTacToe()
    game2 = TicTacToe()

    x_player_minimax = GeniusComputerPlayer('X', use_alpha_beta=False)
    o_player_random = RandomComputerPlayer('O')

    x_player_alpha_beta = GeniusComputerPlayer('X', use_alpha_beta=True)
    o_player_random2 = RandomComputerPlayer('O')

    start_minimax = time.time()
    play(game1, x_player_minimax, o_player_random, print_game=False)
    end_minimax = time.time()

    start_alpha_beta = time.time()
    play(game2, x_player_alpha_beta, o_player_random2, print_game=False)
    end_alpha_beta = time.time()

    print(f"Minimax Execution Time: {end_minimax - start_minimax:.4f} seconds")
    print(f"Alpha-Beta Execution Time: {end_alpha_beta - start_alpha_beta:.4f} seconds")

if __name__ == '__main__':
    compare_performance()


    x_player = HumanPlayer('X')
    o_player = GeniusComputerPlayer('O', use_alpha_beta=True)
    t = TicTacToe()
    play(t, x_player, o_player)
