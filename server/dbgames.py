from models import User, MGame
from main import db

from cleardb import reset

reset()

lines = [l.strip() for l in open("games.txt").readlines()]

NAMES = "Marten Robin Arndt Jördis Enzio Dirk Tino Steffen Philip".split()
NAMES = {n[0]:n for n in NAMES}
NAMES["Z"] = "Esther"
NAMES["I"] = "Simon"
NAMES["L"] = "Marlene"

for v in NAMES.values():
    u = User(username=v)
    u.set_password(v)
    db.session.add(u)

for l in lines:
    p1 = User.query.filter_by(username=NAMES[l[0]]).first()
    p2 = User.query.filter_by(username=NAMES[l[2]]).first()

    if " " in l:
        n = int(l.split("x")[-1])
    else:
        n = 1

    for i in range(n):
        g = MGame(owner=p1.id, winner=p1.id, p1=p1.id, p2=p2.id, ranked=1, accepted=1)
        db.session.add(g)
db.session.commit()
