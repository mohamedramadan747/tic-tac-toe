import os
import random
import time


class Menu:

    @staticmethod
    def display_main_menu():
        main_menu = f"""
WELCOME TO X-O GAME
1. Start game
2. Computer mode
3. Quit game
"""
        while True:
            choice = input(main_menu)
            if not choice.isdigit() or choice not in ['1', '2', '3']:
                print('INVALID CHOICE')
                continue
            return choice

    @staticmethod
    def display_endgame_menu():
        end_game = """
1. Restart
2. Quit game
"""
        while True:
            choice = input(end_game)
            if not choice.isdigit() or choice not in ['1', '2']:
                print('INVALID CHOICE')
                continue
            return choice


class Player:

    Players = []
    Symbols = []

    def __init__(self):
        self.name = ''
        self.symbol = ''

    def choose_name(self):
        while True:
            name = input('ENTER YOUR NAME: ')
            if not name.isalpha() or name in Player.Players:
                print('INVALID NAME OR ALREADY TAKEN')
                continue
            self.name = name.title()
            Player.Players.append(name)
            return

    def choose_symbol(self):
        while True:
            symbol = input('Enter your symbol: ')
            if not symbol.isalpha() or len(symbol) != 1 or symbol in Player.Symbols:
                print('INVALID SYMBOL')
                print(f'CHOOSE ANOTHER SYMBOL' if symbol in Player.Symbols else "MUST BE SINGLE LETTER")
                continue
            self.symbol = symbol.upper()
            Player.Symbols.append(symbol)
            return


class Board:
    def __init__(self):
        self.board = []

    def display_board(self):
        if len(self.board) < 10:
            for i in range(0, 10, 3):
                print('    |    '.join(self.board[i:i+3]))
                if i < 6:
                    print('-'*23)
        else:
            for i in range(0, 17, 4):
                print('    |    '.join(self.board[i:i+4]))
                if i < 9:
                    print('-'*37)

    def choose_board(self):
        while True:
            Game.clear_screen()
            choice = input('1. BIG BOARD\n2. SMALL BOARD: ')
            if not choice.isdigit() or choice not in ['1', '2']:
                print(f'Please enter 1 or 2')
                continue
            self.board = [str(i) for i in range(1, 10)] if choice == '2' else [str(i).zfill(2) for i in range(1, 17)]
            break

    def choosing_box(self):
        while True:
            box = input('Choose Box: (you have 5 second) ')
            if box.isdigit() and 0 < int(box) <= len(self.board) and self.board[int(box) - 1].isdigit():
                return int(box) - 1
            print(f'INVALID BOX')

    def update_board(self, index, symbol):
        self.board[index] = f' {symbol}' if self.is_big_board() else symbol

    def reset_board(self):
        self.board = [str(i).zfill(2) for i in range(1, 17)] if self.is_big_board() else [str(i) for i in range(1, 10)]
        Game.clear_screen()

    def check_win(self):
        sb_win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        bb_win_conditions = [
            [0, 1, 2], [1, 2, 3],
            [4, 5, 6], [5, 6, 7],
            [8, 9, 10], [9, 10, 11],
            [12, 13, 14], [13, 14, 15],
            [0, 4, 8], [4, 8, 12],
            [1, 5, 9], [5, 9, 13],
            [2, 6, 10], [6, 10, 14],
            [3, 7, 11], [7, 11, 15],
            [2, 5, 8], [3, 6, 9], [6, 9, 12], [7, 10, 13],
            [1, 6, 11], [0, 5, 10], [5, 10, 15], [4, 9, 14]
        ]
        board = bb_win_conditions if self.is_big_board() else sb_win_conditions
        while True:
            for row in board:
                if self.board[row[0]] == self.board[row[1]] == self.board[row[2]]:
                    self.shading_win_line(row)
                    return True
            return False

    def check_draw(self):
        return ''.join(self.board).isalpha()

    def shading_win_line(self, line):
        for i in line:
            self.board[i] = '✔'
        self.display_board()

    def is_big_board(self):
        return len(self.board) > 9


class Game:

    def __init__(self):
        self.board = Board()
        self.players = []
        self.menu = Menu()
        self.current_player_index = 0
        self.computer_mode = False

    def setup_players(self):
        player1 = Player()
        player2 = Player()
        self.players.extend((player1, player2)) if not self.computer_mode else self.players.append(player1)
        for index, player in enumerate(self.players, 1):
            print(f'Player{index} Enter details: ')
            player.choose_name()
            player.choose_symbol()
            self.clear_screen()

    def play_game(self):
        while True:
            player = self.players[self.current_player_index]
            self.view_player(player)
            if self.board.check_win() or self.board.check_draw():
                self.drawl() if self.board.check_draw() else self.game_over() if self.computer_mode else self.display_winner()
                option = self.menu.display_endgame_menu()
                if option == '1':
                    self.board.reset_board()
                    continue
                self.quit_game()
                break
            self.board.display_board()
            start_time = time.time()
            box = self.board.choosing_box()
            last_time = time.time()
            timer = last_time - start_time
            if timer <= 5:
                self.board.update_board(box, player.symbol)
                self.clear_screen()
            else:
                print(f'TIME OUT')
                print('THIS IS RANDOM CHOICE')
                self.computer_play() if self.computer_mode else self.switch_player()
                self.random_move(player.symbol)

    def computer_play(self):
        if self.board.check_win() or self.board.check_draw():
            self.display_winner() if self.board.check_win() else self.drawl()
            option = self.menu.display_endgame_menu()
            if option == '1':
                self.board.reset_board()
            elif option == '2':
                self.quit_game()
            return
        lista = [int(i) for i in self.board.board if i.isdigit()]
        box = random.choice(lista) - 1
        self.board.update_board(box, '#')

    def start_game(self):
        choice = self.menu.display_main_menu()
        if choice == '1':
            self.setup_players()
            self.board.choose_board()
            self.play_game()
        elif choice == '2':
            self.computer_mode = True
            self.setup_players()
            self.board.choose_board()
            self.play_game()
        else:
            self.quit_game()

    def random_move(self, symbol):
        lista = [int(i) for i in self.board.board if i.isdigit()]
        random_box = random.choice(lista)
        self.board.update_board(random_box, symbol)

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def display_winner(self):
        if not self.computer_mode:
            self.switch_player()
        player = self.players[self.current_player_index]
        print(f'CONGRATULATION. ❤❤❤')
        print(f'WINNER IS {player.name} WITH SYMBOL: {player.symbol}')
        print('-'*30)
        self.board.display_board()
        print('-'*30)

    def game_over(self):
        self.clear_screen()
        self.board.display_board()
        print('-'*30)
        print(f'GAME OVER')
        print(f'You Lose')
        print('-'*30)

    @classmethod
    def clear_screen(cls):
        os.system('cls')

    @staticmethod
    def quit_game():
        print(f'Thank you for playing.')

    @staticmethod
    def drawl():
        print('DRAWL GAME')
        print(f'NO WINNER')

    @staticmethod
    def view_player(player):
        print(f'{player.name} Turn =====> {player.symbol}')
        print('-'*37)


game = Game()
game.start_game()


# todo: add computer player mode   ✔
# todo: make sure computer symbol not match with player symbol  ✔
# todo: add timer for each player and punish if out time by random step  ✔


def hello(name):
    return f'hello {name}'

