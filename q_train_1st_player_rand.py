from ast import literal_eval
from datetime import datetime
from  subprocess import PIPE,Popen
from time import time
import pandas as pd
from Connect4.connect_4_board import ConnectFour
import numpy as np

GAMES =2
counter =0

def write_values (wins, draws,lost,avg_time,reward,n_games=0):
    date_value =datetime.now().strftime('%d/%m/%Y %H:%M').replace(' ',',')
    process = Popen(['tail','-n','1','Connect4/TrainningData/games_q_1st_rand.csv'],stdout=PIPE)
    try:
        last_game = int(process.stdout.readlines())[0].decode('UTF-8').split(',')[2]
    except:
        last_game=0
    with open('TrainningData/games_q_1st_rand.csv', 'a') as games_file:
        games_file.write(
            f'\n{date_value},{last_game+n_games},{wins},{draws},{avg_time},{lost},{reward}')

qdict = {}
table = pd.read_csv('TrainningData/q_learning_table_1st_rand.csv')

for i in range(len(table['states'])):
    qdict[table['states'][i]] = literal_eval(table['scores'][i])


while True:
    wins = draws = lost=0
    max_time = 0
    min_time = np.PINF
    average = 0
    process = Popen(['tail', '-n', '1', 'Connect4/TrainningData/games_q_1st_rand.csv'], stdout=PIPE)
    games = int(process.stdout.readlines()[
        0].decode('UTF-8').split(',')[2])
    if games < 150:
        eps_0 = 0.3
    else:
        eps_0 = -1

    for i in range(1, GAMES + 1):

        print(f'Game {i}:')
        start = time()
        game = ConnectFour()
        game.Q_learn_Training_2nd_player_random(qdict, eps_0)
        end = time()
        time_spent = end - start
        print('Delta_t:', f'{round(time_spent, 1)}s')

        if game.winner == 1:
            wins += 1
        elif game.winner is None:
            draws += 1
        else:
            lost+=1

        average += time_spent / GAMES


    print('Victoires', wins)
    print("lost",lost)
    print("drAW",draws)
    print(f'AVG: {round(average,1)}')

    d = {'states': [], 'scores': []}
    df = pd.DataFrame(d)
    states, scores = [], []

    for i in qdict.keys():
        states.append(i)
        scores.append(qdict[i])

    df['states'] = states
    df['scores'] = scores
    df['scores'].sum()
    df.to_csv('Connect4/TrainningData/q_learning_table_1st_rand.csv', index=False)
    write_values( wins, draws, round(average, 1),lost,list(df['scores']),GAMES)
    counter = counter+1
    print("counter", counter)
    if(counter>2):
        break



