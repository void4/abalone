from main import MGame, User, db

print(MGame.query.delete())
db.session.commit()
