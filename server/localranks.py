from trueskill import Rating, rate_1vs1, quality_1vs1
from copy import deepcopy
from collections import Counter, defaultdict

lines = [l.strip() for l in open("games.txt").readlines()]

games = []

history = []

players = set()

NAMES = "Marten Robin Arndt Jördis Enzio Dirk Tino Steffen Philip".split()
NAMES = {n[0]:n for n in NAMES}
NAMES["Z"] = "Esther"
NAMES["I"] = "Simon"
NAMES["L"] = "Marlene"

for l in lines:
    p1 = l[0]
    p2 = l[2]

    players.add(p1)
    players.add(p2)


    if " " in l:
        n = int(l.split("x")[-1])
    else:
        n = 1

    for i in range(n):
        games.append([p1, p2])

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

from math import sqrt
from trueskill import BETA
from trueskill.backends import cdf

def win_probability2(greater, lesser):
    exp = (greater.mu - lesser.mu) / BETA
    n = 4. ** exp
    return n / (n + 1)

def win_probability(player_rating, opponent_rating):
    delta_mu = player_rating.mu - opponent_rating.mu
    denom = sqrt(2 * (BETA * BETA) + pow(player_rating.sigma, 2) + pow(opponent_rating.sigma, 2))
    return cdf(delta_mu / denom)

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

import matplotlib.pyplot as plt

for p,d in sorted(players.items(), key=lambda x:x[1]["r"].mu, reverse=True):
    #print(p, d)

    X = []
    Y = []
    for hi, h in enumerate(history):
        X.append(hi)
        Y.append(h[p]["r"].mu)#-3*h[p]["r"].sigma)#viz uncertainty as well!

    mu = d['r'].mu
    sigma = d['r'].sigma
    numgames = d['g']
    plt.plot(X,Y,label=NAMES[p]+" %.2f+-%.2f %i" % (mu, sigma, numgames))

plt.legend()
plt.show()
