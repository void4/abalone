from models import User, MGame
from copy import deepcopy
from trueskill import Rating, rate_1vs1
from collections import defaultdict, Counter
import hashlib


def colorFromName(name):
    #cache this somewhere...
    #maybe compute this clientside?
    hash_object = hashlib.sha256(name.encode("utf-8"))
    hex_dig = hash_object.hexdigest()
    r = int(hex_dig[-2:], 16)
    g = int(hex_dig[-4:-2], 16)
    b = int(hex_dig[-6:-4], 16)
    a = 1.0
    return f"rgba({r},{g},{b},{a})"

def getStats():
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


    #print(len(history))

    datasets = []

    multiplier = 40#1

    for p,d in sorted(players.items(), key=lambda x:x[1]["r"].mu, reverse=True):
        #print(p, d)

        X = []
        Y = []
        for hi, h in enumerate(history):
            X.append(hi)
            Y.append({"x":hi, "y":h[p]["r"].mu*multiplier})#-2*h[p]["r"].sigma})##viz uncertainty as well!

        mu = d['r'].mu*multiplier
        sigma = d['r'].sigma*multiplier
        numgames = d['g']

        line = {
          "label": p+" %.2f+-%.2f (%i games)" % (mu, sigma, numgames),
          "fill": False,
          "data": Y,
          "borderColor": colorFromName(p),
        }

        datasets.append(line)

    print(datasets)
    return datasets
