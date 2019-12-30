from models import MGame, User
from main import db

moves = open("6out.game").read()

moves = "\n".join(moves.split("\n")[:-1])


a = User.query.filter_by(username="Arndt").first()
m = User.query.filter_by(username="Marten").first()

g = MGame(owner=a.id, p1=m.id, p2=a.id, moves=moves, ranked=1)

db.session.add(g)
db.session.commit()
