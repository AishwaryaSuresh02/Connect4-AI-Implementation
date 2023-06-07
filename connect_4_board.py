from copy import deepcopy
from random import choice
import random
from sys import exit
import numpy as np
from pygame import MOUSEBUTTONDOWN, MOUSEMOTION, QUIT, display, draw
from pygame import event as pygame_event
from pygame import font
from pygame import init as pygame_init
from pygame import time as pygame_time
from alpha_beta_pruning import get_moves, probable_next_state, min_max_algo, hard_coded_best_moves, \
    move_according_min_max_algo, probable_next_state_for_q

# Constants
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)


class ConnectFour:
    BOARD_ROW = 6
    BOARD_COLUMN = 7
    '''
    Creating 6X& size connect 4 board
    '''

    def __init__(self):
        self.row = self.BOARD_ROW
        self.col = self.BOARD_COLUMN
        self.connect_4_board = np.zeros((self.BOARD_ROW, self.BOARD_COLUMN))
        self.game_over = False
        self.player_turn = 0
        self.winner = None
        self.loser = None
        self.draw = None

    def print_connect_4_board(self):
        print(np.flip(self.connect_4_board, 0))

    def draw_board(self, screen):
        height = (self.row + 1) * SQUARESIZE

        for c in range(self.col):
            for r in range(self.row):
                draw.rect(
                    screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                draw.circle(screen, BLACK, (int(
                    c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

        for c in range(self.col):
            for r in range(self.row):
                if self.connect_4_board[r][c] == 1:
                    draw.circle(screen, RED, (int(
                        c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                elif self.connect_4_board[r][c] == 2:
                    draw.circle(screen, YELLOW, (int(
                        c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
        display.update()

    '''
       Assigning Value 1 or 2 based on the move made by player 1 or player 2 
    '''

    def assign_move(self, row_val, col_val, player_value):
        if self.connect_4_board[row_val][col_val] == 0:
            self.connect_4_board[row_val][col_val] = player_value
        else:
            print("Invalid Move")

    '''
    Check If the move Made by the user is valid , This is done by checking if the elements in that column is empty or not 
    '''

    def is_move_valid(self, player_choosed_col):
        flag = (self.connect_4_board[self.row - 1][player_choosed_col] == 0) and (player_choosed_col < self.col)
        return flag

    '''
     Function helps to get the  row values which is empty for the given column , min value of all the avaliable space in the row is sent , as the coins should be stack on each other
    '''

    def get_available_row(self, col):
        for row_number in range(self.row):
            if int(self.connect_4_board[int(row_number)][int(col)]) == 0:
                return int(row_number)
        return -1

    '''Print the board'''

    def connect_4_board_print(self):
        print(np.flip(self.connect_4_board, 0))

    ''' 
     Check if the there are same 4 coins present row wise or column wise or diagonally 
    '''

    def check_if_player_is_winner(self, player_choosed_coin):
        # Check if there are 4 coins in any rows present
        for in_col in range(self.col - 3):
            for in_row in range(self.row):
                if self.connect_4_board[in_row][in_col] == player_choosed_coin and \
                        self.connect_4_board[in_row][in_col + 1] == player_choosed_coin and \
                        self.connect_4_board[in_row][in_col + 2] == player_choosed_coin and \
                        self.connect_4_board[in_row][in_col + 3] == player_choosed_coin:
                    return True
        # Check if the coins are present in any columns
        for in_row in range(self.row - 3):
            for in_col in range(self.col):
                if self.connect_4_board[in_row][in_col] == player_choosed_coin and \
                        self.connect_4_board[in_row + 1][in_col] == player_choosed_coin and \
                        self.connect_4_board[in_row + 2][in_col] == player_choosed_coin and \
                        self.connect_4_board[in_row + 3][in_col] == player_choosed_coin:
                    return True

        # Check if the coins are present diagonally
        for in_row in range(self.row - 3):
            for in_col in range(self.col - 3):
                if self.connect_4_board[in_row][in_col] == player_choosed_coin and \
                        self.connect_4_board[in_row + 1][in_col + 1] == player_choosed_coin and \
                        self.connect_4_board[in_row + 2][in_col + 2] == player_choosed_coin and \
                        self.connect_4_board[in_row + 3][in_col + 3] == player_choosed_coin:
                    return True

        # Chcek if the coins is present in the anti diaginally
        for in_col in range(self.col - 3):
            for in_row in range(3, self.row):
                if self.connect_4_board[in_row][in_col] == player_choosed_coin and \
                        self.connect_4_board[in_row - 1][in_col + 1] == player_choosed_coin and \
                        self.connect_4_board[in_row - 2][in_col + 2] == player_choosed_coin and \
                        self.connect_4_board[in_row - 3][in_col + 3] == player_choosed_coin:
                    return True

        return False

    ''' Convert Connect 4 Board to array'''

    def board_to_string(self):
        ''' Returns ndarray board as string'''
        connect_4_str = ''

        for in_row in range(self.row):
            for in_col in range(self.col):
                connect_4_str += str(int(self.connect_4_board[in_row][in_col]))

        return connect_4_str

    ''' If String is given convert to connect 4 board '''

    def string_to_board(self, board_str):

        for in_row in range(self.rows):
            for in_col in range(self.cols):
                self.connect_4_board[in_row][in_col] = float(board_str[self.cols * in_row + in_col])

    '''
    Checks If there is any empty place in connect four board , sends true if all the places are filled up else false
    '''

    def if_board_is_full(self):
        for in_col in range(self.col):
            for in_row in range(self.row):
                if self.connect_4_board[in_row][in_col] == 0:
                    return False
        return True

    '''
    Check if the game is over , Game is considered as  over if there is a winner or no places , retruns flag and number of the player 1 or player 2 in case there are winner else returns 0 , -1 is sent if the game is not over
    '''

    def check_if_game_is_over(self):

        if self.check_if_player_is_winner(1):
            # Player 1 is the winner
            return True, 1
        elif self.check_if_player_is_winner(2):
            # Player 2 is the winner
            return True, 2
        elif self.if_board_is_full():
            #  Board is full but  no winners
            return True, 0
        else:
            # Board is not full game is still on
            return False - 1

    '''
        Get the Peak of the given column (Can be used to decide the next move )
    '''

    def row_peak(self, col_to_be_checked):
        for row_int in range(self.row - 1, -1, -1):
            cell_value = self.connect_4_board[row_int][col_to_be_checked]
            if cell_value != 0:
                return cell_value
        return 0

    '''
            Get the Peak of the given column (Can be used to decide the next move )
        '''

    def col_peak(self, row_to_checked):
        for col_int in range(self.col):
            cell_value = self.connect_4_board[row_to_checked][col_int]
            if cell_value != 0:
                return cell_value, col_int
        return 0, -1

    '''
        Sends True if the intended colum is full else false
    '''

    def check_col_full(self, col_to_be_checked):
        for in_row in range(self.row):
            if self.connect_4_board[in_row][col_to_be_checked] == 0:
                return False
        return True

    '''
           Sends True if the intended row is full else false
       '''

    def check_row_full(self, row_to_checked):
        for in_col in range(self.col):
            if self.connect_4_board[row_to_checked][in_col] == 0:
                return False
        return True

    '''
     Returns the colum number  of which the player has to place his coin
    '''

    def get_cover_player(self, player_choice_coin):
        """
        Returns the index of the column (0-indexed) of which this player wants to place his token
        """

        otherPlayer = 1 if (player_choice_coin == 2) else 2
        cover_1 = -1
        cover_2 = -1

        # try to cover the other player's tokens
        for col in range(self.col):
            if self.row_peak(col) == otherPlayer and not self.check_col_full(col):
                cover_1 = col
                break

        for row in range(self.row):
            cell_value, col_value = self.col_peak(int(row))
            if col_value != -1:
                if cell_value == otherPlayer and not self.check_row_full(int(row)) and not self.check_col_full(
                        col_value):
                    cover_2 = col_value
                    break

        if cover_1 != -1:
            if cover_2 != -1:
                return random.choice([cover_1, cover_2])
            else:
                return int (cover_1)
        else:
            if cover_2 != -1:
                return int(cover_2)

        for col in range(self.col):
            if not self.check_col_full(col):
                return int(col)

    def get_valid_moves(self):
        list_of_moves = set()
        for in_col in range(self.col):
            if self.is_move_valid(in_col):
                list_of_moves.add(in_col)
            if len(list_of_moves) == 0:
                self.game_over = True
        return list_of_moves

    '''
        Return a random move 
    '''

    def get_random_player(self):
        if not self.if_board_is_full():
            counter = 0
            while True:
                col_value_choosed = choice(range(0, self.col))
                if not self.check_col_full(col_value_choosed):
                    return col_value_choosed
                counter = counter + 1
                if counter > 7:
                    break
            return -1
        return -1

    def play(self):
        '''Allows you to play as Player 2 against Minimax'''

        pygame_init()

        width = self.col * SQUARESIZE
        height = (self.row + 1) * SQUARESIZE
        size = (width, height)

        screen = display.set_mode(size)
        self.draw_board(screen)
        display.update()

        myfont = font.Font('sweet purple.ttf', 75)

        choice_value = random.choice([0, 1])

        if choice_value:

            while not self.game_over:
                for event in pygame_event.get():
                    if event.type == QUIT:
                        exit()
                    if event.type == MOUSEMOTION:
                        draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                        posx = event.pos[0]
                        if self.player_turn:
                            col = self.get_cover_player(2)
                            print("temp_value", col)
                            row = self.get_available_row(int(col))
                            print("row", row)
                            self.assign_move(row, col, 2)

                            if self.check_if_player_is_winner(2):
                                label = myfont.render("COMP wins!", 2, YELLOW)
                                screen.blit(label, (width / 4, 10))
                                self.game_over = True
                                self.draw_board(screen)
                                break
                            self.draw_board(screen)
                            self.player_turn = 1 - self.player_turn

                        else:
                            draw.circle(
                                screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                        display.update()

                    if event.type == MOUSEBUTTONDOWN:
                        draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                        # Asks for Player's input
                        if not self.player_turn:
                            # Turn = 1
                            posx = event.pos[0]
                            col = int(posx / SQUARESIZE)
                            if self.is_move_valid(col):
                                row = self.get_available_row(col)
                                self.assign_move(row, col, 1)

                                if self.check_if_player_is_winner(1):
                                    label = myfont.render(
                                        "Player wins!", 1, RED)
                                    screen.blit(label, (width / 4, 10))
                                    self.game_over = True
                                    self.draw_board(screen)
                                    break

                            self.draw_board(screen)
                            self.player_turn = 1 - self.player_turn
        else:
            while not self.game_over:
                for event in pygame_event.get():
                    if event.type == QUIT:
                        exit()
                    if event.type == MOUSEMOTION:
                        draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                        posx = event.pos[0]
                        if self.player_turn == 0:
                            col = move_according_min_max_algo(self)
                            row = self.get_available_row(col)
                            self.assign_move(row, col, 1)

                            if self.check_if_player_is_winner(1):
                                label = myfont.render("COMP wins!", 1, RED)
                                screen.blit(label, (width / 4, 10))
                                self.game_over = True
                                self.draw_board(screen)
                                break
                            self.draw_board(screen)
                            self.player_turn = 1 - self.player_turn

                        else:
                            draw.circle(
                                screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                        display.update()

                    if event.type == MOUSEBUTTONDOWN:
                        draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                        # Asks for Player's input
                        if not self.player_turn:
                            # Turn = 0
                            pass

                        else:
                            # Turn = 1
                            posx = event.pos[0]
                            col = int(posx / SQUARESIZE)
                            if self.is_move_valid(col):
                                row = self.get_available_row(col)
                                self.assign_move(row, col, 2)

                                if self.check_if_player_is_winner(2):
                                    label = myfont.render(
                                        "Player wins!", 1, YELLOW)
                                    screen.blit(label, (width / 4, 10))
                                    self.game_over = True
                                    self.draw_board(screen)
                                    break

                            self.draw_board(screen)
                            self.player_turn = 1 - self.player_turn

        pygame_time.wait(5000)

    '''
    Helps to play against random cover player
    '''

    def play_cover(self):
        '''Allows you to play as Player 2 against Minimax'''

        pygame_init()

        width = self.col * SQUARESIZE
        height = (self.row + 1) * SQUARESIZE
        size = (width, height)

        screen = display.set_mode(size)
        self.draw_board(screen)
        display.update()

        myfont = font.Font('sweet purple.ttf', 75)

        while not self.game_over:
            for event in pygame_event.get():
                if event.type == QUIT:
                    exit()
                if event.type == MOUSEMOTION:
                    draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if self.player_turn == 0:
                        col = self.get_cover_player(1)
                        row = self.get_available_row(col)
                        self.assign_move(row, col, 1)

                        if self.check_if_player_is_winner(1):
                            label = myfont.render("COMP wins!", 1, RED)
                            screen.blit(label, (width / 4, 10))
                            self.game_over = True
                            self.draw_board(screen)
                            break
                        self.draw_board(screen)
                        self.player_turn = 1 - self.player_turn

                    else:
                        draw.circle(
                            screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                    display.update()

                if event.type == MOUSEBUTTONDOWN:
                    draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                    # Asks for Player's input
                    if not self.player_turn:
                        # Turn = 0
                        pass

                    else:
                        # Turn = 1
                        posx = event.pos[0]
                        col = int(posx / SQUARESIZE)
                        if self.is_move_valid(col):
                            row = self.get_available_row(col)
                            self.assign_move(row, col, 2)

                            if self.check_if_player_is_winner(2):
                                label = myfont.render(
                                    "Player wins!", 1, YELLOW)
                                screen.blit(label, (width / 4, 10))
                                self.game_over = True
                                self.draw_board(screen)
                                break

                        self.draw_board(screen)
                        self.player_turn = 1 - self.player_turn

        pygame_time.wait(5000)

    '''Original'''

    def org_play(self):
        '''Allows you to play as Player 2 against Minimax'''

        pygame_init()

        width = self.col * SQUARESIZE
        height = (self.row + 1) * SQUARESIZE
        size = (width, height)

        screen = display.set_mode(size)
        self.draw_board(screen)
        display.update()

        myfont = font.Font('sweet purple.ttf', 75)

        while not self.game_over:
            for event in pygame_event.get():
                if event.type == QUIT:
                    exit()
                if event.type == MOUSEMOTION:
                    draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if self.player_turn == 1:
                        col = move_according_min_max_algo(self)
                        print("col", col)
                        row = self.get_available_row(col)
                        self.assign_move(row, col, 2)

                        if self.check_if_player_is_winner(2):
                            label = myfont.render("Minimax wins!", 1, RED)
                            screen.blit(label, (width / 4, 10))
                            self.game_over = True
                            self.draw_board(screen)
                            break
                        self.draw_board(screen)
                        self.player_turn = 1 - self.player_turn

                    else:
                        draw.circle(
                            screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                    display.update()

                if event.type == MOUSEBUTTONDOWN:
                    draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                    # Asks for Player's input
                    if self.player_turn:
                        # Turn = 0
                        pass

                    else:
                        # Turn = 1
                        posx = event.pos[0]
                        col = int(posx / SQUARESIZE)
                        if self.is_move_valid(col):
                            row = self.get_available_row(col)
                            self.assign_move(row, col, 1)

                            if self.check_if_player_is_winner(1):
                                label = myfont.render(
                                    "Player wins!", 1, YELLOW)
                                screen.blit(label, (width / 4, 10))
                                self.game_over = True
                                self.draw_board(screen)
                                break

                        self.draw_board(screen)
                        self.player_turn = 1 - self.player_turn

        pygame_time.wait(5000)

    def org_play_first(self):
        '''Allows you to play as Player 2 against Minimax'''

        pygame_init()

        width = self.col * SQUARESIZE
        height = (self.row + 1) * SQUARESIZE
        size = (width, height)

        screen = display.set_mode(size)
        self.draw_board(screen)
        display.update()

        myfont = font.Font('sweet purple.ttf', 75)

        while not self.game_over:
            for event in pygame_event.get():
                if event.type == QUIT:
                    exit()
                if event.type == MOUSEMOTION:
                    draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if self.player_turn == 0:
                        col = move_according_min_max_algo(self)
                        print("col", col)
                        row = self.get_available_row(col)
                        self.assign_move(row, col, 1)

                        if self.check_if_player_is_winner(1):
                            label = myfont.render("Minimax wins!", 1, RED)
                            screen.blit(label, (width / 4, 10))
                            self.game_over = True
                            self.draw_board(screen)
                            break
                        self.draw_board(screen)
                        self.player_turn = 1 - self.player_turn

                    else:
                        draw.circle(
                            screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                    display.update()

                if event.type == MOUSEBUTTONDOWN:
                    draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                    # Asks for Player's input
                    if not self.player_turn:
                        # Turn = 0
                        pass

                    else:
                        # Turn = 1
                        posx = event.pos[0]
                        col = int(posx / SQUARESIZE)
                        if self.is_move_valid(col):
                            row = self.get_available_row(col)
                            self.assign_move(row, col, 1)

                            if self.check_if_player_is_winner(1):
                                label = myfont.render(
                                    "Player wins!", 1, YELLOW)
                                screen.blit(label, (width / 4, 10))
                                self.game_over = True
                                self.draw_board(screen)
                                break

                        self.draw_board(screen)
                        self.player_turn = 1 - self.player_turn

        pygame_time.wait(5000)

    def play_cop(self):
        '''Allows you to play as Player 2 against Minimax'''

        pygame_init()

        width = self.col * SQUARESIZE
        height = (self.row + 1) * SQUARESIZE
        size = (width, height)

        screen = display.set_mode(size)
        self.draw_board(screen)
        display.update()

        myfont = font.Font('sweet purple.ttf', 75)

        while not self.game_over:
            for event in pygame_event.get():
                if event.type == QUIT:
                    exit()
                if event.type == MOUSEMOTION:
                    draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if self.player_turn == 0:
                        col = move_according_min_max_algo(self)
                        row = self.get_available_row(col)
                        self.assign_move(row, col, 1)

                        if self.check_if_player_is_winner(1):
                            label = myfont.render("Minimax wins!", 1, RED)
                            screen.blit(label, (width / 4, 10))
                            self.game_over = True
                            self.draw_board(screen)
                            break
                        self.draw_board(screen)
                        self.player_turn = 1 - self.player_turn

                    else:
                        draw.circle(
                            screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                    display.update()

                if event.type == MOUSEBUTTONDOWN:
                    draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                    # Asks for Player's input
                    if not self.player_turn:
                        # Turn = 0
                        pass

                    else:
                        # Turn = 1
                        posx = event.pos[0]
                        col = int(posx / SQUARESIZE)
                        if self.is_move_valid(col):
                            row = self.get_available_row(col)
                            self.assign_move(row, col, 2)

                            if self.check_if_player_is_winner(2):
                                label = myfont.render(
                                    "Player wins!", 1, YELLOW)
                                screen.blit(label, (width / 4, 10))
                                self.game_over = True
                                self.draw_board(screen)
                                break

                        self.draw_board(screen)
                        self.player_turn = 1 - self.player_turn

        pygame_time.wait(5000)

    def org_play_min_max_vs_rand(self):

        while not self.game_over:
            if self.player_turn == 0:
                col = move_according_min_max_algo(self)
                row = self.get_available_row(col)
                self.assign_move(row, col, 1)

                if self.check_if_player_is_winner(1):
                            self.game_over = True
                            break

                self.player_turn = 1 - self.player_turn

            else :
                col = self.get_cover_player(2)
                row = self.get_available_row(col)
                self.assign_move(row, col, 2)

                if self.check_if_player_is_winner(2):
                    self.game_over = True
                    break
                self.player_turn = 1 - self.player_turn

    def org_rand_vs_min_max(self):

        while not self.game_over:
            if self.player_turn == 1:
                col = move_according_min_max_algo(self)
                row = self.get_available_row(col)
                self.assign_move(row, col, 2)

                if self.check_if_player_is_winner(2):
                    self.game_over = True
                    break

                self.player_turn = 1 - self.player_turn

            else:
                col = self.get_cover_player(1)
                row = self.get_available_row(col)
                self.assign_move(row, col, 1)

                if self.check_if_player_is_winner(1):
                    self.game_over = True
                    break
                self.player_turn = 1 - self.player_turn

    def org_play_rand_vs_qlearn(self,qdict):

        '''Allows you to play as Player 1 against our trained model'''

        while not self.game_over:
            if self.player_turn == 1:
                state = self.board_to_string()
                try:
                    score = qdict[state]
                    col = score.index(max(score))
                except:
                    col = choice(list(get_moves(self)))

                row = self.get_available_row(col)
                self.assign_move(row, col, 2)

                if self.check_if_player_is_winner(2):
                    self.game_over = True
                    break
                self.player_turn = 1 - self.player_turn

            else:
                col = self.get_cover_player(1)
                if(col== None):
                    if (self.if_board_is_full()):
                        self.game_over== True
                        self.winner= None
                        break

                row = self.get_available_row(col)
                self.assign_move(row, col, 1)

                if self.check_if_player_is_winner(1):
                    self.game_over = True
                    break
                self.player_turn = 1 - self.player_turn

    def org_play_q_first_vs_rand(self,qdict):

        '''Allows you against our trained model against rand'''

        while not self.game_over:
            if self.player_turn == 0:
                state = self.board_to_string()
                try:
                    score = qdict[state]
                    col = score.index(max(score))
                except:
                    col = choice(list(get_moves(self)))

                row = self.get_available_row(col)
                self.assign_move(row, col, 1)

                if self.check_if_player_is_winner(1):
                    self.game_over = True
                    break
                self.player_turn = 1 - self.player_turn

            else:
                col = self.get_cover_player(2)
                row = self.get_available_row(col)
                self.assign_move(row, col, 2)

                if self.check_if_player_is_winner(2):
                    self.game_over = True
                    break
                self.player_turn = 1 - self.player_turn


    def q_player_vs_min_max(self,qdict):

        '''Allows q player against min max'''

        while not self.game_over:
            if self.player_turn == 0:
                state = self.board_to_string()
                try:
                    score = qdict[state]
                    col = score.index(max(score))
                except:
                    col = choice(list(get_moves(self)))

                row = self.get_available_row(col)
                self.assign_move(row, col, 1)

                if self.check_if_player_is_winner(1):
                    self.game_over = True
                    break
                self.player_turn = 1 - self.player_turn

            else:
                col = move_according_min_max_algo(self)
                row = self.get_available_row(col)
                self.assign_move(row, col, 2)

                if self.check_if_player_is_winner(2):
                    self.game_over = True
                    break
                self.player_turn = 1 - self.player_turn


    def min_max_vs_q_player(self,qdict):

        '''Allows q player against min max'''

        while not self.game_over:
            if self.player_turn == 1:
                state = self.board_to_string()
                try:
                    score = qdict[state]
                    col = score.index(max(score))
                except:
                    col = choice(list(get_moves(self)))

                row = self.get_available_row(col)
                self.assign_move(row, col, 2)

                if self.check_if_player_is_winner(2):
                    self.game_over = True
                    break
                self.player_turn = 1 - self.player_turn

            else:
                col = move_according_min_max_algo(self)
                row = self.get_available_row(col)
                self.assign_move(row, col, 1)

                if self.check_if_player_is_winner(1):
                    self.game_over = True
                    break
                self.player_turn = 1 - self.player_turn



    def Q_learn_Training_1st_player_min_max(self, q_values_dic, eplison_threshold):
        # Consider Aplha and Gamma Values
        ALPHA = 0.5
        GAMMA = 0.9

        while not self.game_over:
            explore = False
            if not self.player_turn :
                col = move_according_min_max_algo(self)
                row = self.get_available_row(col)
                self.assign_move(row,col,1)
                if self.check_if_player_is_winner(1):
                    self.game_over=True
                    self.winner=0
                self.player_turn=1
            else:
                coin_states = self.board_to_string()
                possible_list_moves = self.get_valid_moves()
                possible_next_state_moves, possible_min_max_moves = probable_next_state_for_q(self)
                if not coin_states in q_values_dic.keys():
                    # check if the current state is already present in the q_dict_values sent as the
                    q_values_dic[coin_states] = [0] * self.col

                # current state q-vqlue
                Q_list = deepcopy(q_values_dic[coin_states])
                eplison = random.uniform(0, 1)

                if eplison < eplison_threshold:
                    # Do explorition
                    explore = True
                    choose_col = choice(list(possible_list_moves))
                else:
                    for int_col in range(self.col):
                        if int_col not in possible_list_moves:
                            Q_list[int_col] = np.NINF
                    choose_col = Q_list.index(max(Q_list))

                last_state_q_value = (1 - ALPHA) * Q_list[choose_col]

                # Q makes Player moves
                pic_row = self.get_available_row(choose_col)
                self.assign_move(pic_row, choose_col, 2)
                self.player_turn = 0

                if self.check_if_player_is_winner(2):
                    q_values_dic[coin_states][choose_col] = 1
                    self.winner = 1
                    self.game_over = True
                elif not possible_min_max_moves:
                    self.game_over= True
                    q_reward = 1 / 42
                    if not explore:
                        new_update_value = last_state_q_value + (ALPHA * q_reward)
                        q_values_dic[coin_states][choose_col] = float(f'{new_update_value:5f}')
                else:
                    predict_move = possible_min_max_moves[str(choose_col)]
                    if not predict_move:
                        predict_move=random.choice(list(self.get_valid_moves()))
                    row_predict = self.get_available_row(predict_move)
                    self.assign_move(row_predict, predict_move, 1)
                    self.player_turn = 1
                    if self.check_if_player_is_winner(1):
                        q_values_dic[coin_states][choose_col] = -1
                        self.winner = 0
                        self.game_over = True
                    else:
                        try:
                            maximum_q_value = max([q_values_dic[self.board_to_string()][col_int] for col_int in
                                                       self.get_valid_moves()])
                        except:
                            q_values_dic[coin_states] = [0] * self.col
                            maximum_q_value = 0
                        q_reward = 1 / 42
                        if not explore:
                            new_update_value = last_state_q_value + (ALPHA * q_reward) + (
                                        ALPHA * maximum_q_value * GAMMA)
                            q_values_dic[coin_states][choose_col] = float(f'{new_update_value:5f}')


    def Q_learn_Training_2nd_player_min_max(self, q_values_dic, eplison_threshold):
        # Consider Aplha and Gamma Values
        ALPHA = 0.5
        GAMMA = 0.9

        while not self.game_over:
            explore = False
            if self.player_turn:
                col = move_according_min_max_algo(self)
                row = self.get_available_row(col)
                self.assign_move(row, col, 2)
                if self.check_if_player_is_winner(2):
                    self.game_over = True
                    self.winner = 1
                self.player_turn = 0
            else:
                coin_states = self.board_to_string()
                possible_list_moves = self.get_valid_moves()
                possible_next_state_moves, possible_min_max_moves = probable_next_state_for_q(self)
                if not coin_states in q_values_dic.keys():
                    # check if the current state is already present in the q_dict_values sent as the
                    q_values_dic[coin_states] = [0] * self.col

                # current state q-vqlue
                Q_list = deepcopy(q_values_dic[coin_states])
                eplison = random.uniform(0, 1)

                if eplison < eplison_threshold:
                    # Do explorition
                    explore = True
                    choose_col = choice(list(possible_list_moves))
                else:
                    for int_col in range(self.col):
                        if int_col not in possible_list_moves:
                            Q_list[int_col] = np.NINF
                    choose_col = Q_list.index(max(Q_list))

                last_state_q_value = (1 - ALPHA) * Q_list[choose_col]

                # Q makes Player moves
                pic_row = self.get_available_row(choose_col)
                self.assign_move(pic_row, choose_col, 1)
                self.player_turn = 1

                if self.check_if_player_is_winner(1):
                    q_values_dic[coin_states][choose_col] = 1
                    self.winner = 0
                    self.game_over = True
                elif not possible_min_max_moves:
                    self.game_over = True
                    q_reward = 1 / 42
                    if not explore:
                        new_update_value = last_state_q_value + (ALPHA * q_reward)
                        q_values_dic[coin_states][choose_col] = float(f'{new_update_value:5f}')
                else:
                    predict_move = possible_min_max_moves[str(choose_col)]
                    if not predict_move:
                        predict_move =random.choice( list(self.get_valid_moves()))
                    row_predict = self.get_available_row(predict_move)
                    self.assign_move(row_predict, predict_move, 2)
                    self.player_turn = 0
                    if self.check_if_player_is_winner(2):
                        q_values_dic[coin_states][choose_col] = -1
                        self.winner = 1
                        self.game_over = True
                    else:
                        try:
                            maximum_q_value = max([q_values_dic[self.board_to_string()][col_int] for col_int in
                                                   self.get_valid_moves()])
                        except:
                            q_values_dic[coin_states] = [0] * self.col
                            maximum_q_value = 0
                        q_reward = 1 / 42
                        if not explore:
                            new_update_value = last_state_q_value + (ALPHA * q_reward) + (
                                    ALPHA * maximum_q_value * GAMMA)
                            q_values_dic[coin_states][choose_col] = float(f'{new_update_value:5f}')

    def Q_learn_Training_2nd_player_random(self, q_values_dic, eplison_threshold):
        # Consider Aplha and Gamma Values
        ALPHA = 0.5
        GAMMA = 0.9

        while not self.game_over:
            explore = False
            if self.player_turn:
                col = self.get_cover_player(2)
                row = self.get_available_row(col)
                self.assign_move(row, col, 2)
                if self.check_if_player_is_winner(2):
                    self.game_over = True
                    self.winner = 1
                self.player_turn = 0
            else:
                coin_states = self.board_to_string()
                possible_list_moves = self.get_valid_moves()
                possible_next_state_moves, possible_min_max_moves = probable_next_state_for_q(self)
                if not coin_states in q_values_dic.keys():
                    # check if the current state is already present in the q_dict_values sent as the
                    q_values_dic[coin_states] = [0] * self.col

                # current state q-vqlue
                Q_list = deepcopy(q_values_dic[coin_states])
                eplison = random.uniform(0, 1)

                if eplison < eplison_threshold:
                    # Do explorition
                    explore = True
                    choose_col = choice(list(possible_list_moves))
                else:
                    for int_col in range(self.col):
                        if int_col not in possible_list_moves:
                            Q_list[int_col] = np.NINF
                    choose_col = Q_list.index(max(Q_list))

                last_state_q_value = (1 - ALPHA) * Q_list[choose_col]

                # Q makes Player moves
                pic_row = self.get_available_row(choose_col)
                self.assign_move(pic_row, choose_col, 1)
                self.player_turn = 1

                if self.check_if_player_is_winner(1):
                    q_values_dic[coin_states][choose_col] = 1
                    self.winner = 0
                    self.game_over = True
                elif not possible_min_max_moves:
                    self.game_over = True
                    q_reward = 1 / 42
                    if not explore:
                        new_update_value = last_state_q_value + (ALPHA * q_reward)
                        q_values_dic[coin_states][choose_col] = float(f'{new_update_value:5f}')
                else:
                    predict_move = possible_min_max_moves[str(choose_col)]
                    if not predict_move:
                        predict_move =random.choice( list(self.get_valid_moves()))
                    row_predict = self.get_available_row(predict_move)
                    self.assign_move(row_predict, predict_move, 2)
                    self.player_turn = 0
                    if self.check_if_player_is_winner(2):
                        q_values_dic[coin_states][choose_col] = -1
                        self.winner = 1
                        self.game_over = True
                    else:
                        try:
                            maximum_q_value = max([q_values_dic[self.board_to_string()][col_int] for col_int in
                                                   self.get_valid_moves()])
                        except:
                            q_values_dic[coin_states] = [0] * self.col
                            maximum_q_value = 0
                        q_reward = 1 / 42
                        if not explore:
                            new_update_value = last_state_q_value + (ALPHA * q_reward) + (
                                    ALPHA * maximum_q_value * GAMMA)
                            q_values_dic[coin_states][choose_col] = float(f'{new_update_value:5f}')

    def Q_learn_Training_1st_player_random(self, q_values_dic, eplison_threshold):
        # Consider Aplha and Gamma Values
        ALPHA = 0.5
        GAMMA = 0.9

        while not self.game_over:
            explore = False
            if not self.player_turn :
                col = self.get_cover_player(1)
                row = self.get_available_row(col)
                self.assign_move(row,col,1)
                if self.check_if_player_is_winner(1):
                    self.game_over=True
                    self.winner=0
                self.player_turn=1
            else:
                coin_states = self.board_to_string()
                possible_list_moves = self.get_valid_moves()
                possible_next_state_moves, possible_min_max_moves = probable_next_state_for_q(self)
                if not coin_states in q_values_dic.keys():
                    # check if the current state is already present in the q_dict_values sent as the
                    q_values_dic[coin_states] = [0] * self.col

                # current state q-vqlue
                Q_list = deepcopy(q_values_dic[coin_states])
                eplison = random.uniform(0, 1)

                if eplison < eplison_threshold:
                    # Do explorition
                    explore = True
                    choose_col = choice(list(possible_list_moves))
                else:
                    for int_col in range(self.col):
                        if int_col not in possible_list_moves:
                            Q_list[int_col] = np.NINF
                    choose_col = Q_list.index(max(Q_list))

                last_state_q_value = (1 - ALPHA) * Q_list[choose_col]

                # Q makes Player moves
                pic_row = self.get_available_row(choose_col)
                self.assign_move(pic_row, choose_col, 2)
                self.player_turn = 0

                if self.check_if_player_is_winner(2):
                    q_values_dic[coin_states][choose_col] = 1
                    self.winner = 1
                    self.game_over = True
                elif not possible_min_max_moves:
                    self.game_over= True
                    q_reward = 1 / 42
                    if not explore:
                        new_update_value = last_state_q_value + (ALPHA * q_reward)
                        q_values_dic[coin_states][choose_col] = float(f'{new_update_value:5f}')
                else:
                    predict_move = possible_min_max_moves[str(choose_col)]
                    if not predict_move:
                        predict_move=random.choice(list(self.get_valid_moves()))
                    row_predict = self.get_available_row(predict_move)
                    self.assign_move(row_predict, predict_move, 1)
                    self.player_turn = 1
                    if self.check_if_player_is_winner(1):
                        q_values_dic[coin_states][choose_col] = -1
                        self.winner = 0
                        self.game_over = True
                    else:
                        try:
                            maximum_q_value = max([q_values_dic[self.board_to_string()][col_int] for col_int in
                                                       self.get_valid_moves()])
                        except:
                            q_values_dic[coin_states] = [0] * self.col
                            maximum_q_value = 0
                        q_reward = 1 / 42
                        if not explore:
                            new_update_value = last_state_q_value + (ALPHA * q_reward) + (
                                        ALPHA * maximum_q_value * GAMMA)
                            q_values_dic[coin_states][choose_col] = float(f'{new_update_value:5f}')