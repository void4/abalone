from collections import Counter, defaultdict
from copy import deepcopy
from math import sqrt

from trueskill import Rating, rate_1vs1, quality_1vs1
from trueskill import BETA
from trueskill.backends import cdf

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from models import MGame, User

def win_probability2(greater, lesser):
    exp = (greater.mu - lesser.mu) / BETA
    n = 4. ** exp
    return n / (n + 1)

def win_probability(player_rating, opponent_rating):
    delta_mu = player_rating.mu - opponent_rating.mu
    denom = sqrt(2 * (BETA * BETA) + pow(player_rating.sigma, 2) + pow(opponent_rating.sigma, 2))
    return cdf(delta_mu / denom)

def generatePlot(path):
    plt.figure(figsize=(20,10))
    #TODO optimize mgames = MGame.query.having(winner=True)
    mgames = [mg for mg in MGame.query.all() if mg.winner != None and mg.ranked != 0]
    print(mgames)
    games = [[User.query.get(mg.winner).username, User.query.get(mg.p1 if mg.winner == mg.p2 else mg.p2).username] for mg in mgames]

    history = []

    players = set([u.username for u in User.query.all()])

    players = {p:{"r":Rating(), "g":0} for p in players}

    vsgames = defaultdict(Counter)
    for gi, g in enumerate(games):
        p1 = g[0]
        p2 = g[1]

        vsgames[p1][p2] += 1
        vsgames[p2][p1] += 1

        r1 = players[p1]["r"]
        r2 = players[p2]["r"]

        players[p1]["r"], players[p2]["r"] = rate_1vs1(r1, r2)

        players[p1]["g"] += 1
        players[p2]["g"] += 1

        history.append(deepcopy(players))

    for p,d in vsgames.items():
        print(p, d.most_common())



    matrix = "   "

    for p2 in players:
        matrix += p2 + "   "

    matrix += "\n"

    for p1,p1d in players.items():
        matrix += p1 + " "
        for p2,p2d in players.items():
            p1r = p1d["r"]
            p2r = p2d["r"]
            # This is the DRAW probability
            #q = quality_1vs1(p1r, p2r)
            # This is the WIN probability
            q = win_probability(p1r, p2r)
            matrix += ("%.0f%% " % (q*100)).zfill(4)
        matrix += "\n"

    print(matrix)

    #print(quality_1vs1(players["E"]["r"], players["A"]["r"]))
    print(len(history))
    #print(sum([v["r"].mu for v in players.values()])/len(players))


    for p,d in sorted(players.items(), key=lambda x:x[1]["r"].mu, reverse=True):
        #print(p, d)

        X = []
        Y = []
        for hi, h in enumerate(history):
            X.append(hi)
            Y.append(h[p]["r"].mu)#XXX -2*h[p]["r"].sigma)#viz uncertainty as well!

        mu = d['r'].mu
        sigma = d['r'].sigma
        numgames = d['g']
        plt.plot(X,Y,label=p+" %.2f+-%.2f %i" % (mu, sigma, numgames))

    plt.legend()
    plt.savefig(path)
    plt.close()
    #plt.show()

if __name__ == "__main__":
    generatePlot("../client/src/assets/graph.png")
