from connect_4_board import *
import pandas as pd
import ast

count = 0
result_stats = {
    "Q_learning": 0,
    "DEFAULT": 0,
    "Draw": 0
}
Q_table = {}
table = pd.read_csv('/Users/aishwaryasuresh/PycharmProjects/Connect4_1/q_learning_table.csv')
for i in range(len(table['states'])):
    Q_table[table['states'][i]] = ast.literal_eval(table['scores'][i])
while count < 1000:

    val = random.choice([1, 2])
    print(val)
    if val == 1:
        '''rand as 1st player'''
        game = ConnectFour()
        game.org_play_rand_vs_qlearn(Q_table)
        if game.check_if_player_is_winner(1):
            result_stats['DEFAULT'] = (result_stats['DEFAULT']) + 1
        elif game.check_if_player_is_winner(2):
            result_stats['Q_learning'] = (result_stats['Q_learning']) + 1
        else:
            result_stats['Draw'] = (result_stats['Draw']) + 1
    else:
        '''Random Min Max '''
        game = ConnectFour()
        game.org_play_q_first_vs_rand(Q_table)
        if game.check_if_player_is_winner(2):
            result_stats['DEFAULT'] = (result_stats['DEFAULT']) + 1
        elif game.check_if_player_is_winner(1):
            result_stats['Q_learning'] = (result_stats['Q_learning']) + 1
        else:
            result_stats['Draw'] = (result_stats['Draw']) + 1

    count = count + 1
print(result_stats)
