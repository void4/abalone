from models import User, MGame
from copy import deepcopy
from trueskill import Rating, rate_1vs1
from collections import defaultdict, Counter
import hashlib


def colorFromName(name, alpha=1.0):
    #cache this somewhere...
    #maybe compute this clientside?
    hash_object = hashlib.sha256(name.encode("utf-8"))
    hex_dig = hash_object.hexdigest()
    r = int(hex_dig[-2:], 16)
    g = int(hex_dig[-4:-2], 16)
    b = int(hex_dig[-6:-4], 16)
    return f"rgba({r},{g},{b},{alpha})"

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
        # Upper and lower bounds respectively
        U = []
        D = []
        # Point radii
        R = []
        for hi, h in enumerate(history):
            mu = h[p]["r"].mu*multiplier
            sigma = h[p]["r"].sigma*multiplier*0.3
            pointradius = "transparent" if history[hi-1][p]["r"].mu*multiplier==mu else "#ffffff"
            R.append(pointradius)
            X.append(hi)
            Y.append({"x":hi, "y":mu})#, "radius": pointradius
            U.append({"x":hi, "y":mu+sigma})
            D.append({"x":hi, "y":mu-sigma})

        mu = d['r'].mu*multiplier
        sigma = d['r'].sigma*multiplier
        numgames = d['g']

        line = {
          "label": p+" %.2f+-%.2f (%i games)" % (mu, sigma, numgames),
          "fill": False,
          "data": Y,
          "tension": 0,
          "borderColor": colorFromName(p),
          "pointBorderColor": R,
          "pointBackgroundColor": R,
        }
        up = {
          "fill": len(datasets),
          "data": U,
          "backgroundColor": colorFromName(p, 0.2),
          "borderColor": "transparent",
          "pointRadius": 0,
          "tension": 0,
        }
        down = {
          "fill": len(datasets),
          "data": D,
          "backgroundColor": colorFromName(p, 0.2),
          "borderColor": "transparent",
          "pointRadius": 0,
          "tension": 0,
        }
        datasets.append(line)
        #datasets.append(up)
        #datasets.append(down)

    #print(datasets)
    return datasets
