from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)#TODO case insensitive
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)

class MGame(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    #created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    owner = db.Column(db.Integer, db.ForeignKey("user.id"))
    p1 = db.Column(db.Integer, db.ForeignKey("user.id"))
    p2 = db.Column(db.Integer, db.ForeignKey("user.id"))
    moves = db.Column(db.Text)
    winner = db.Column(db.Integer, db.ForeignKey("user.id"))
    lastmove = db.Column(db.DateTime, default=datetime.utcnow)
    ranked = db.Column(db.Integer, default=0)
    accepted = db.Column(db.Integer, default=1)

    def addMove(self, movestr):
        if self.moves is None:
            self.moves = ""
        self.moves += "%s\n" % movestr

        self.lastmove = datetime.utcnow()

    def __repr__(self):
        return "<Game {}>".format(self.id)
