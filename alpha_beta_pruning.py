from copy import deepcopy
import numpy as np
import random


def find_indices(list_to_check, item_to_find):
    array = np.array(list_to_check)
    indices = np.where(array == item_to_find)[0]
    return list(indices)

''' Retrun all the columns in the board where a  possible move can be made '''


def get_moves(ConnectFour):
    list_of_moves = set()
    for in_col in range(ConnectFour.col):
        if ConnectFour.is_move_valid(in_col):
            list_of_moves.add(in_col)
    if len(list_of_moves) == 0:
        ConnectFour.game_over = True
    return list_of_moves


''' Gives all the state till the end by traversing '''


def probable_next_state(ConnectFour):
    dict_probable_move = {}
    for col_int in ConnectFour.get_valid_moves():
        Next_State = deepcopy(ConnectFour)
        result_row = Next_State.get_available_row(col_int)
        opponent_piece = Next_State.player_turn + 1
        Next_State.assign_move(result_row, col_int, opponent_piece)
        #  Checks if the Next move results in lossing
        if (Next_State.check_if_player_is_winner(opponent_piece)) or (not (Next_State.get_valid_moves)):
            Next_State.game_over = True
        # Storing Status of next move for all the colum of the board status
        dict_probable_move[str(col_int)] = Next_State
    if not dict_probable_move and ConnectFour.game_over:
        ConnectFour.game_over = True
    return dict_probable_move


'''Implementing Min max algorithm with alpha beta purning'''


def min_max_algo(ConnectFour, tree_depth, alpha_val, beta_val, IsMaximizingPlayer=None):
    #  Player playing one is considered as maximize player else its minmaizing logic
    if IsMaximizingPlayer == None:
        if not ConnectFour.player_turn:
            IsMaximizingPlayer = True
        else:
            IsMaximizingPlayer = False

    if not tree_depth or ConnectFour.game_over:
        return hard_coded_best_moves(ConnectFour)
        #  Max Finding logic
    elif IsMaximizingPlayer:
        max_value = -float('inf')
        for probable_states in probable_next_state(ConnectFour).values():
            # since max was call next state is min
            temp = min_max_algo(probable_states, tree_depth - 1, alpha_val, beta_val, False)
            max_value = max(max_value, temp)
            alpha_val = max(alpha_val, temp)
            if beta_val <= alpha_val:
                # No need to search furture in the loop
                break
        return max_value

    else:
        min_value = float('inf')
        for probable_states in probable_next_state(ConnectFour).values():
            #  Since Min is called next state will be max
            temp = min_max_algo(probable_states, tree_depth - 1, alpha_val, beta_val, True)
            min_value = min(min_value, temp)
            beta_val = min(beta_val, temp)
            if beta_val <= alpha_val:
                break
        return min_value


'''
     hard Coded  Best moves  evaluation
'''


def hard_coded_best_moves(ConnectFour):
    SCORE = 0
    player_2_token_mapping = {1: 1, 2: -1}
    good_positions = [{'1110', '1101', '1011', '0111'},
                      {'2220', '2202', '2022', '0222'}]
    win_positions = ['1111', '2222']

    for piece in [1, 2]:

        # Checks if good position is present row wise
        for row_int in range(ConnectFour.row):
            ROW = str(int(ConnectFour.connect_4_board[row_int][0]))
            for col_int in range(1, ConnectFour.col):
                ROW += str(int(ConnectFour.connect_4_board[row_int][col_int]))
            for start_index in range(len(ROW) - 3):
                if ROW[start_index:start_index + 4] in good_positions[piece - 1]:
                    SCORE += player_2_token_mapping[piece] * 10
                if ROW[start_index:start_index + 4] in win_positions[piece - 1]:
                    SCORE += player_2_token_mapping[piece] * 1000
        # Checks  Values in the  columns
        for col_int in range(ConnectFour.col):
            COL = str(int(ConnectFour.connect_4_board[0][col_int]))
            for row_int in range(1, ConnectFour.row):
                COL += str(int(ConnectFour.connect_4_board[row_int][col_int]))
            for start_index in range(len(COL) - 3):
                if COL[start_index:start_index + 4] in good_positions[piece - 1]:
                    SCORE += player_2_token_mapping[piece] * 10
                if COL[start_index:start_index + 4] in win_positions[piece - 1]:
                    SCORE += player_2_token_mapping[piece] * 1000

        # Check if good position is found in the Diagonals
        for col_int in range(ConnectFour.col - 3):
            for row_int in range(ConnectFour.row - 3):
                diagonal = str(int(ConnectFour.connect_4_board[row_int][col_int]))
                for i in range(1, 4):
                    diagonal += str(int(ConnectFour.connect_4_board[row_int + i][col_int + i]))
                for start_index in range(len(diagonal) - 3):
                    if diagonal[start_index:start_index + 4] in good_positions[piece - 1]:
                        SCORE += player_2_token_mapping[piece] * 10
                    if diagonal[start_index:start_index + 4] in win_positions[piece - 1]:
                        SCORE += player_2_token_mapping[piece] * 1000

        # Check if good positions are present in Anti-Diagonal
        for col_int in range(ConnectFour.col - 3):
            for row_int in range(3, ConnectFour.row):
                anti_diagonal = str(int(ConnectFour.connect_4_board[row_int][col_int]))
                for i in range(1, 4):
                    anti_diagonal += str(int(ConnectFour.connect_4_board[row_int - i][col_int + i]))
                for start_index in range(len(anti_diagonal) - 3):
                    if anti_diagonal[start_index:start_index + 4] in good_positions[piece - 1]:
                        SCORE += player_2_token_mapping[piece] * 10
                    if anti_diagonal[start_index:start_index + 4] in win_positions[piece - 1]:
                        SCORE += player_2_token_mapping[piece] * 1000

    return SCORE


''' Returns approriate move according to the min max algorithm'''


def move_according_min_max_algo(ConnectFour):
    if not ConnectFour.game_over:
        possible_moves_list = ConnectFour.get_valid_moves()
        # Selecting a Esplion value
        epslion = random.uniform(0, 1)
        if epslion < 0.05:
            # Exploration Phase
            return random.choice(list(possible_moves_list))
        else:
            #  When Player is playin as first player and 1 is assigned
            if not ConnectFour.player_turn:
                # Player Should always choose Max so making a array with negative infinite
                scores = [-float('inf')] * ConnectFour.col
            else:
                # Player Is playing second so must choose Min , so making array with inifinty
                scores = [float('inf')] * ConnectFour.col

            states = probable_next_state(ConnectFour)
            for state in states.keys():
                te=min_max_algo(states[state], 3, -float('inf'), float('inf'),
                                                   not (states[state].player_turn))

                scores[int(state)] = min_max_algo(states[state], 3, -float('inf'), float('inf'),
                                                   not (states[state].player_turn))

            absoulte_scores = list()
            for ele in scores:
                absoulte_scores.append(abs(ele))
            # scores=absoulte_scores
            #  Finding Which index has max score
            high_probable_max_move = find_indices(scores,max(scores))
            high_probable_min_move = find_indices(scores,min(scores))

            # Checking for invalid moves and making them as Nan in score list
            for col_int in range(ConnectFour.col):
                if col_int not in possible_moves_list:
                    scores[col_int] = float('nan')

            if ConnectFour.player_turn == 0:
                # Max Scores needs to be selected
                if abs(np.nanmean(scores)) != float('inf'):
                    # Checking if any invalid move is present before maximizing the score
                    if max(scores) == int(np.nanmean(scores)):
                        # All the moves have equal score
                        if not max(scores) or 3 in possible_moves_list:
                            move = 3  # consider 3 as its the middle of the board and gets more weightage
                            return move
                        else:
                            move = random.choice(list(possible_moves_list))
                            return move
                    else:
                        if len(high_probable_max_move)>1:
                            move = random.choice(high_probable_max_move)
                            return move
                        else:
                            move = high_probable_max_move[0]
                            return move


                else:
                    ConnectFour.print_connect_4_board()
                    print("ScoresValues", scores)
                    print("Possible Moves", possible_moves_list)
                    print("Is it game over", ConnectFour.game_over)
                    bug_file = open('TrainningData/bug_reports.txt', 'a')
                    bug_file.write('Coups: ' + str(ConnectFour) + '\n')
                    bug_file.write('Scores: ' + str(scores) + '\n')
                    bug_file.write('Board: ' + ConnectFour.board_to_string() + '\n')
                    bug_file.write('Game Over: ' +
                                   str(ConnectFour.game_over) + '\n')
                    bug_file.write(' ')
                    bug_file.close()
                    # send a random  possible move
                    move = random.choice(list(possible_moves_list))
                    return move
            else:
                # player should be minizized
                if abs(np.mean(scores)) != float('inf'):
                    # Checking if any invalid move is present before maximizing the score
                    if min(scores) == int(np.nanmean(scores)):
                        # All the moves have equal score
                        if not min(scores) or 3 in possible_moves_list:
                            move = 3  # consider 3 as its the middle of the board and gets more weightage
                            return move
                        else:
                            move = random.choice(list(possible_moves_list))
                            return move
                    else:
                        if len(high_probable_min_move) > 1:
                            move = random.choice(high_probable_min_move)
                            return move
                        else:
                            move = high_probable_min_move[0]
                            return move

                else:
                    ConnectFour.print_connect_4_board()
                    print("ScoresValues", scores)
                    print("Possible Moves", possible_moves_list)
                    print("Is it game over", ConnectFour.game_over)
                    # bug_file = open('bug_reports.txt', 'a')
                    # bug_file.write('Coups: ' + str(list(ConnectFour)) + '\n')
                    # bug_file.write('Scores: ' + str(scores) + '\n')
                    # bug_file.write('Board: ' + ConnectFour.board_to_string() + '\n')
                    # bug_file.write('Game Over: ' +
                    #                str(ConnectFour.game_over) + '\n')
                    # bug_file.write(' ')
                    # bug_file.close()
                    # send a random  possible move
                    move = random.choice(list(possible_moves_list))
                    return move


def probable_next_state_for_q(ConnectFour):
    dict_propable_moves = {}
    dict_min_max_move = {}
    for col_int in ConnectFour.get_valid_moves():
        Next_State = deepcopy(ConnectFour)
        row_int = Next_State.get_available_row(col_int)
        opponent_piece = ConnectFour.player_turn + 1
        Next_State.assign_move(row_int, col_int, opponent_piece)
        Next_State.player_turn = 1 - Next_State.player_turn
        if Next_State.check_if_player_is_winner(opponent_piece) or (not Next_State.get_valid_moves()):
            Next_State.game_over = True
        else:
            col_int_2 = move_according_min_max_algo(Next_State)
            dict_min_max_move[str(col_int)] = col_int_2
            try:
                row_int_2 = Next_State.get_available_row(col_int_2)
            except:
                col_int_2 = random.choice(list(Next_State.get_valid_moves()))
                if not col_int_2:
                    Next_State.game_over=True
                    dict_propable_moves[str(col_int)] = Next_State
                    break
                row_int_2 = Next_State.get_available_row(col_int_2)
            peiec = Next_State.player_turn + 1
            Next_State.assign_move(row_int_2, col_int_2, peiec)
            Next_State.player_turn = 1 - Next_State.player_turn
            if Next_State.check_if_player_is_winner(peiec) or (not Next_State.get_valid_moves()):
                Next_State.game_over = True
        dict_propable_moves[str(col_int)] = Next_State
    if not dict_propable_moves and not ConnectFour.game_over:
        ConnectFour.game_over = True
    return dict_propable_moves, dict_min_max_move
