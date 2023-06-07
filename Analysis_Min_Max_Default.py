from connect_4_board import *
count =0
result_stats = {
        "MIN_MAX": 0,
        "DEFAULT": 0,
        "Draw": 0
    }
while count < 1000:

    val = random.choice([1,2])
    if val==1:
        '''Min Max as 1st player'''
        game = ConnectFour()
        game.org_play_min_max_vs_rand()
        if game.check_if_player_is_winner(1):
            result_stats['MIN_MAX']=(result_stats['MIN_MAX'])+1
        elif game.check_if_player_is_winner(2):
            result_stats['DEFAULT'] = (result_stats['DEFAULT']) + 1
        else :
            result_stats['Draw'] = (result_stats['Draw']) + 1
    else:
        '''Random Min Max '''
        game = ConnectFour()
        game.org_rand_vs_min_max()
        if game.check_if_player_is_winner(2):
            result_stats['MIN_MAX'] = (result_stats['MIN_MAX']) + 1
        elif game.check_if_player_is_winner(1):
            result_stats['DEFAULT'] = (result_stats['DEFAULT']) + 1
        else:
            result_stats['Draw'] = (result_stats['Draw']) + 1

    count=count+1
    print("count",count)
print(result_stats)




