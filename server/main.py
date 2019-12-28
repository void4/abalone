from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
from random import randint, choice
import json
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(Config)

app.config['JWT_SECRET_KEY'] = "C6SBm83gDenAZJbx4fUX9"
jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

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

    def __repr__(self):
        return "<Game {}>".format(self.id)

login = LoginManager(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

CORS(app, resources={r'/*': {"origins": "*"}})

@app.route("/register")
def route_register():
    username = request.args.get("username")
    password = request.args.get("password")
    user = User(username=username)
    user.set_password(password)
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({"info":"registered!", "status":"success"})
    except Exception as e:
        print(e)
    return jsonify({"info":"registration failed.", "status":"fail"})

@app.route("/login")
def route_login():
    username = request.args.get("username")
    password = request.args.get("password")
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({"info":"Invalid username or password"})

    access_token = create_access_token(identity=username)
    return jsonify({"info":"logged in!", "status":"success", "token":access_token})

def getRequestUser():
    username = get_jwt_identity()
    print("Authenticated user", username)
    user = User.query.filter_by(username=username).first()
    return user

@app.route("/auth")
@jwt_required
def route_auth():
    print(request.args)
    print(getRequestUser())
    return jsonify({})

@app.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify(str(randint(0,9)))

@app.route("/name", methods=["GET"])
def name():
    return jsonify(choice("ABALONE SCHABLONE ABALTWO".split()))
#, "send_wildcard":True}}, expose_headers=["Access-Control-Allow-Origin"], send_wildcard=True)

from pyabalone.solver import Game, DIRECTIONS
from collections import defaultdict

#defaultdict with timeout?
# check if player is participating
# or spectating is allowed
# by link or by name? (whitelist, invite)
# inviting external, not logged in player? -> unrated
#save game creation date, prune if too old
#-> no winner?
#save creator -> two offline players

def getGame(gid):
    mg = MGame.query.get(gid)
    if mg is None:
        return None
    premoves = mg.moves
    g = Game()
    if isinstance(premoves, str):
    	for line in premoves.split("\n"):
    		line = line.strip()
    		if len(line) == 0:
    			continue
    		#print(line)
    		g.move(*g.move_from_str(line))
    return g


@app.route("/newgame", methods=["GET"])
@jwt_required#shouldn't be REQUIRED, otherwise unregistered users can't use
def newgame():
    user = getRequestUser()
    gamemode = request.args.get("gamemode", "pvp")
    g = MGame()
    g.owner = user.id
    g.p1 = user.id
    if gamemode == "myself":
        g.p2 = user.id
    elif gamemode == "pvp":
        #requi
        ranked = 1 if request.args.get("ranked", "true") == "true" else 0
        g.ranked = ranked
        pass
    elif gamemode == "ai":#like pvp, invite ai player?
        pass#g.p2 = ai.id
    else:
        raise Exception("Unknown gamemode", gamemode)
        #g.p2 =
    db.session.add(g)
    db.session.commit()
    return jsonify({"invitelink":"/play/"+str(g.id)})

@app.route("/chat")
@jwt_required
def chat():
    user = getRequestUser()
    msg = request.args.get("chatinput", "")
    if len(msg) > 0:
        print(user.username, ">", msg)
    return jsonify({"chat":msg+"\n"})

@app.route("/gamelist")
@jwt_required
def gamelist():
    user = getRequestUser()
    games = [{"id":g.id} for g in MGame.query.filter_by(owner=user.id)]
    return jsonify({
        "info": "loaded",
        "games": games
    })

@app.route("/game", methods=["GET"])
def game():
    gameid = request.args.get("id", None)
    if gameid is None:
        return jsonify({"info":"No GameID"})

    g = getGame(gameid)
    mg = MGame.query.get(gameid)

    if g is None or mg is None:
        return jsonify({"info":"Game not found"})



    if not g.is_over():
        movestr = request.args.get("move", None)

        moveinfo = ""
        if movestr:
            if movestr.startswith("["):
                movej = json.loads(movestr)
                if len(movej[0]) > 0:
                    selected = ",".join([g.board[index].name for index in movej[0]])
                    # always from first or last ball? from center?
                    movedir = "?"
                    for d,dv in DIRECTIONS.items():
                        t = g.board[movej[0][-1]].to(dv)
                        if len(movej[0]) == 1:

                            if t.color == g.next_color:
                                t = t.to(dv)
                                if t.color == g.next_color:
                                    t = t.to(dv)

                            if t and t.index == movej[1]:
                                movedir = d.split()[-1]
                                break

                        # sideways moves
                        if len(movej[0]) > 1 and t and t.index == movej[1]:
                            movedir = d.split()[-1]
                            break
                    movestr = selected + " " + movedir
            # Can't move if game is over
            move = g.move_from_str(movestr)
            result = g.move(*move)
            if result[0]:

                if mg.moves is None:
                    mg.moves = ""
                mg.moves += "%s\n" % movestr

                mg.lastmove = datetime.utcnow()
                # does this update?

                if g.is_over():
                    outs = list(g.out.items())
                    if outs[0][1] == 6:
                        # Player 0 won
                        mg.winner = mg.p1
                    else:
                        # Player 1 won
                        mg.winner = mg.p2

                db.session.commit()
            moveinfo = str(result)

    moveinfo = "Game Over!"
    p1 = User.query.get(mg.p1) if mg.p1 else None
    p2 = User.query.get(mg.p2) if mg.p2 else None
    p1n = p1.username if p1 else "Unknown"
    p2n = p2.username if p2 else "unknown"
    print("ranked", mg.ranked)
    ranked = False if mg.ranked == 0 else True

    state = [[field.xycoords, field.color] for field in g.board]

    return jsonify({"board":g.sbs(), "state":state, "info":moveinfo, "gameinfo":{"p1":p1n, "p2":p2n, "ranked":ranked, "next":g.next_color}})#jsonify(str(g))

if __name__ == "__main__":
    app.run()
