from main import MGame, User, db

def reset():
    print("Clearing DB")
    print(User.query.delete())
    print(MGame.query.delete())
    db.session.commit()

if __name__ == "__main__":
    reset()
