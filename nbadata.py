
import json
import numpy as np
input_dim = 11 * 5

def read_my_stats(filename, players):
        '''
            Read mystats.txt, return dataset
        '''
        f = open(filename, 'r')
        X = np.array([]).reshape((0,input_dim))
        y = []
        for line in f:
            parts = line.split('\t')
            names = parts[0].split(' - ')
            y.append(float(parts[1]))
            a = np.array([]).reshape((1,0))
            for n in names:
                name = n.split(',')
                n = [name[1].lower(), name[0].lower()]
                if '_'.join(n) not in players:
                    raise NameError('Player not found')
                else:
                    a = np.concatenate((a, np.array(players['_'.join(n)]).reshape(1,11)), axis=1)
                    # print a

            X = np.concatenate((X, a), axis=0)

        return X, np.array(y).reshape((len(y),1))       

def read_players(filename):
        '''
            Read players.jl
        '''
        players = {}
        f = open(filename, 'r')
        for line in f:

            player = json.loads(line)

            name = '_'.join([s.lower() for s in player['name']])
            # print '[Debugging]:: ', name
            players[name] = [float(s) for i, s in enumerate(player['stats']) if i != 2 and i != 5]
            # players= a[:,[0,1,3,4,6,7,8,9,10,11,12]]
            
        return players
def preprocessing(players):
    '''
        
    '''
    # means = np.zeros((11,))
    # maxvals = np.zeros(11,)
    # for p in players.itervalues():
    #     stat = p
    #     means += stat
        
    #     maxvals = [abs(stat[i]) if abs(stat[i]) > maxvals[i] else maxvals[i] for i in range(11)]
    # means = means / len(players)
    # # print means, maxvals
    # for name in players:
    #     p = players[name]
    #     p -= means
    #     p /= maxvals
    #     players[name] = p
    # print players
    i = 0
    X = np.zeros((len(players), 11))
    for p in players.itervalues():
        X[i,:] = p
        i += 1
    X -= np.mean(X, axis=0)        # zero-centering
    X /= np.std(X, axis=0)          # normalize
    i = 0
    for name in players:
        players[name] = X[i,:]
        i += 1
    # print players

def form_dataset(statsfile, playerfile):
    players = read_players(playerfile)
    preprocessing(players)
    X, y = read_my_stats(statsfile, players)
    print X.shape
    return X, y

def save_json(filename, data):
    with open(filename, 'w') as fp:
        json.dump(data, fp)




