from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_jwt_extended import (
	JWTManager, jwt_required, create_access_token,
	get_jwt_identity
)
import flask_monitoringdashboard as dashboard

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

dashboard.config.init_from(file='dashboard.cfg')
dashboard.bind(app)

from models import db, MGame, User
db.app = app
db.init_app(app)
migrate = Migrate(app, db)

try:
	AIUSER = User.query.filter_by(username="AI").first()
	if not AIUSER:
		AIUSER = User(username="AI")
		print("Added AI user")
	db.session.add(AIUSER)
	db.session.commit()
except Exception as e:
	print(e)

login = LoginManager(app)

from redis import Redis

red = Redis("127.0.0.1")


@login.user_loader
def load_user(id):
	return User.query.get(int(id))

CORS(app, resources={r'/*': {"origins": "*"}})

#TODO broadcast channel upgrade on register too?
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

	tmpid = request.args.get("tmpid")
	# XXX dangerous, broadcast injection anywhere possible rn
	broadcast("u|"+tmpid, "u|"+username)

	access_token = create_access_token(identity=username)
	return jsonify({"info":"logged in!", "status":"success", "token":access_token})

def getRequestUser():
	username = get_jwt_identity()
	#print("Authenticated user", username)
	user = User.query.filter_by(username=username).first()
	return user

@app.route("/ping", methods=["GET"])
def ping_pong():
	return jsonify(str(randint(0,9)))

@app.route("/players")
def route_players():
	return jsonify({"players": [{"name":user.username, "titles":"", "online": user.online} for user in User.query.all()]})
@jwt_required

@app.route("/name", methods=["GET"])
def name():
	return jsonify(choice("ABALONE SCHABLONE ABALTWO".split()))
#, "send_wildcard":True}}, expose_headers=["Access-Control-Allow-Origin"], send_wildcard=True)

from pyabalone.solver import Game, DIRECTIONS, INDEXNAMES
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

	if mg.state is None:
		layout = mg.layout
		g = Game(layout)

		premoves = mg.moves
		if isinstance(premoves, str):
			for line in premoves.split("\n"):
				line = line.strip()
				if line.count(" ") > 1:
					line = line.rsplit(" ", 1)
				else:
					line = [line]
				if len(line[0]) == 0 or line in "leave surrender".split():
					break
				#print(line)
				g.move(*g.move_from_str(line[0]))

	else:
		layout = mg.state
		g = Game(layout)
		#print("LAYOUT", layout)


	# probabilistic check?

	return g

@app.route("/newgame", methods=["GET"])
@jwt_required#shouldn't be REQUIRED, otherwise unregistered users can't use
def newgame():
	user = getRequestUser()
	gamemode = request.args.get("gamemode", "pvp")
	layout = request.args.get("layout")
	timetomove = request.args.get("timetomove")

	g = MGame()

	g.timetomove = timetomove
	g.p1time = timetomove
	g.p2time = timetomove

	g.layout = layout

	g.owner = user.id
	g.p1 = user.id#TODO randomize?
	if gamemode == "myself":
		g.p2 = user.id
	elif gamemode == "pvp":
		invite = request.args.get("invite", None)
		p2 = User.query.filter_by(username=invite).first()
		# TODO can't invite yourself
		if p2:
			if p2.id == user.id:
				raise Exception("Can't invite yourself")
			g.p2 = p2.id
			ranked = 1 if request.args.get("ranked", "true") == "true" else 0
			g.ranked = ranked
			g.accepted = 0
	elif gamemode == "ai":#like pvp, invite ai player?
		g.p2 = AIUSER.id
	else:
		raise Exception("Unknown gamemode", gamemode)
		#g.p2 =
	db.session.add(g)
	db.session.commit()
	return jsonify({"invitelink":"/play/"+str(g.id), "gid":g.id})

@app.route("/inviteresponse")
@jwt_required
def inviteresponse():
	gid = request.args.get("gid")
	mg = MGame.query.get(int(gid))
	gameinfo = getGameInfo(mg)
	if gameinfo["invited"]:
		accepted = request.args.get("accepted") == "true"
		if accepted:
			mg.accepted = True
			db.session.add(mg)
		else:
			db.session.delete(mg)

		db.session.commit()
	return jsonify({})


@app.route("/gamelist")
@jwt_required
def gamelist():
	user = getRequestUser()
	games = [getGameInfo(mg) for mg in MGame.query.filter(((MGame.p1 == user.id) | (MGame.p2 == user.id)) & MGame.winner.is_(None))]
	return jsonify({
		"info": "loaded",
		"games": games
	})

def getGameInfo(mg):
	gid = mg.id
	owner = User.query.get(mg.owner) if mg.owner else None
	p1 = User.query.get(mg.p1) if mg.p1 else None
	p2 = User.query.get(mg.p2) if mg.p2 else None
	on = owner.username if owner else "Unknown"
	p1n = p1.username if p1 else "Unknown"
	p2n = p2.username if p2 else "unknown"
	ranked = False if mg.ranked == 0 else True
	accepted = False if mg.accepted == 0 else True
	layout = mg.layout
	timetomove = mg.timetomove
	user = getRequestUser()
	if user:
		participating = (p1.id == user.id or p2.id == user.id)
		invited = owner.id != user.id and participating and not accepted
		if p1.id == user.id:
			opponent = p2n
		elif p2.id == user.id:
			opponent = p1n
		else:
			opponent = None
	else:
		invited = False
		opponent = on
	return {"gid":gid, "owner":on, "p1":p1n, "p2":p2n, "ranked":ranked, "accepted":accepted, "invited":invited, "opponent":opponent, "layout":layout, "timetomove":timetomove, "p1time": mg.p1time, "p2time": mg.p2time}

def getMovestr(g, movestr):
	movej = json.loads(movestr)
	if len(movej[0]) > 0:
		selected = ",".join([g.board[index].name for index in movej[0]])
		# always from first or last ball? from center?
		movedir = "?"
		for d,dv in DIRECTIONS.items():
			t = g.board[movej[0][-1]].to(dv)
			if len(movej[0]) == 1:

				if t and t.color == g.next_color:
					t = t.to(dv)
					if t and t.color == g.next_color:
						t = t.to(dv)

				if t and t.index == movej[1]:
					movedir = d.split()[-1]
					break

			# sideways moves
			if len(movej[0]) > 1 and t and t.index == movej[1]:
				movedir = d.split()[-1]
				break
		movestr = selected + " " + movedir
	return movestr

from time import time, sleep

@app.route("/game", methods=["GET"])
@jwt_required
def game():
	gameid = request.args.get("id", None)
	if gameid is None:
		return jsonify({"info":"No GameID"})

	g = getGame(gameid)
	#XXX is gameid a string here? doesn't this fail?
	mg = MGame.query.get(gameid)

	if g is None or mg is None:
		return jsonify({"info":"Game not found"})

	real, user = getRequestOrTempUser()

	broadcast("u|"+user.username, "g|"+str(gameid))
	# XXX will the thread subscribe fast enough?

	MOVES = []

	movestr = request.args.get("move", None)
	opponent = mg.p1 if mg.p2 == user.id else mg.p2
	if movestr == "leave":
		if mg.ranked == 0:
			mg.addMove(movestr)
			if opponent is None:
				mg.winner = AIUSER.id#TODO OFFLINEUSER?
			else:
				mg.winner = opponent
			moveinfo = "Player left"

	elif movestr == "surrender":
		mg.addMove(movestr)
		mg.winner = opponent
		moveinfo = "Player surrendered"

	elif (g.next_color == 0 and user.id != mg.p1) or (g.next_color == 1 and user.id != mg.p2):
		moveinfo = "Not your turn!"

	elif not g.is_over():

		moveinfo = ""
		if movestr:
			if movestr.startswith("["):
				movestr = getMovestr(g, movestr)
			# Can't move if game is over
			try:
				move = g.move_from_str(movestr)
			except KeyError:
				move = None
			if move is None:
				raise Exception("invalid move")
			result = g.move(*move)
			moveinfo = str(result)

			if result[0]:

				mg.state = g.getLayout()

				now = datetime.utcnow()
				if mg.moves is None:
					mg.lastmove = now

				over = False
				if mg.timetomove is not None:
					if user.id == mg.p1:
						mg.p1time -= int(now.timestamp() - mg.lastmove.timestamp())#min 1 sec?

					if user.id == mg.p2:
						mg.p2time -= int(now.timestamp() - mg.lastmove.timestamp())

					if mg.p1time < 0:
						mg.addMove("surrender")
						over = True
					elif mg.p2time < 0:
						mg.addMove("surrender")
						over = True

				if not over:

					mg.addMove(movestr)
					# does this update?
					if g.is_over():
						outs = list(g.out.items())
						if outs[0][1] == 6:
							# Player 0 won
							mg.winner = mg.p2
						else:
							# Player 1 won
							mg.winner = mg.p1

					MOVES.append(movestr)

			if not g.is_over():#check for winner?
				if mg.p2 == AIUSER.id:
					aimove, result = g.aimove()
					print(aimove, result)
					if not result[0]:
						moveinfo = "AI can't move!"
						raise Exception(moveinfo)
						# TODO assign winner?
					aimovedir = list(DIRECTIONS.keys())[aimove[1]].split()[-1]
					if isinstance(aimove[0], list):
						aimovefields = ",".join([INDEXNAMES[f.index] for f in aimove[0]])
					else:
						aimovefields = INDEXNAMES[aimove[0].index]
					aimovestr = aimovefields + " " + aimovedir
					print(aimovestr)
					mg.addMove(aimovestr)
					mg.state = g.getLayout()

					if g.is_over():
						outs = list(g.out.items())
						if outs[0][1] == 6:
							# Player 0 won
							mg.winner = mg.p1
						else:
							# Player 1 won
							mg.winner = mg.p2

					#now = datetime.now().replace(microsecond=0).time()
					#broadcast("game"+gameid, '[%s] AI MOVE %s' % (now.isoformat(), aimovestr))#TODO user

	if g.is_over() or mg.winner is not None:
		moveinfo = "Game Over!"

	# TODO db.session.add(mg)?!
	db.session.commit()

	if MOVES:
		now = datetime.now().replace(microsecond=0).time()
		broadcast("g|"+gameid, '[%s] MOVE %s' % (now.isoformat(), MOVES[0]))#TODO user

	state = [[field.xycoords, field.color] for field in g.board]

	gameinfo = getGameInfo(mg)
	return jsonify({"board":g.sbs(), "state":state, "info":moveinfo, "gameinfo":{"next":g.next_color, "out":list(g.out.values()), **gameinfo}})#jsonify(str(g))

def broadcast(channel, message):
	red.publish(channel, message.encode('utf-8'))

@app.route("/chat")
@jwt_required
def chat():
	user = getRequestUser()
	msg = request.args.get("chatinput", "")
	if len(msg) > 0:
		print(user.username, ">", msg)
		now = datetime.now().replace(microsecond=0).time()
		broadcast('chat', '[%s] %s: %s' % (now.isoformat(), user, msg))
	return jsonify({"chat":msg+"\n"})

QUOTES = ""
try:
	QUOTES = open("quotes.txt").read()
except Exceptions as e:
	print(e)
#print(QUOTES)

@app.route("/quote")
def quote():
	quote = choice(QUOTES.split("\n"))
	return jsonify({"quote":quote})

from stats import getStats

@app.route("/ratings")
def route_ratings():
	return jsonify(getStats())

"""
@app.route("/listen")
def route_listen():
	channel = request.args.get("channel")
	broadcast("global", channel)
"""

streamcounter = 0

def event_stream(user):
	user.online = 1
	db.session.commit()
	try:
		print("Starting stream", user)
		global streamcounter
		streamcounter += 1
		esid = streamcounter
		pubsub = red.pubsub()
		#this can't be global, this has to be user specific, otherwise all users will be subscribed!
		#XXX watch out, user could get name 'game'! prefix somehow
		pubsub.subscribe("u|"+user.username)
		pubsub.subscribe('chat')#TODO reenable
		#for message in pubsub.listen():
		while True:
			message = pubsub.get_message()
			if not message:
				#print("No message")
				yield "data: {}\n\n"
				sleep(0.1)
				continue
			print("MSG", esid, user, message["channel"], message["data"], pubsub.channels)
			#print(message["channel"], user.username, message["channel"]==user.username)
			if message["channel"].decode("utf-8").startswith("u|"):# == user.username:
				if isinstance(message["data"], bytes):
					newchannel = message["data"]
					prefix = newchannel.decode("utf-8")[:2]
					if newchannel not in pubsub.channels:
						for channel in pubsub.channels:
							if channel.decode("utf-8").startswith(prefix):
								print("UNSUB", channel)
								pubsub.unsubscribe(channel)
						print("SUB", newchannel)
						pubsub.subscribe(newchannel)
						username = newchannel.decode("utf8")[2:]
						user = User.query.filter_by(username=username).first()
						user.online = 1
						db.session.commit()
			else:
				#print(type(message["data"]))
				#print("STREAM", message)
				# how to prevent double update for mover?
				# let client send unique update id with /game call, send it back, then let client check
				# alternatively, use username-channel, and one public/spectator one
				if isinstance(message["data"], bytes):
					yield 'data: %s\n\n' % json.dumps({"channel": message["channel"].decode("utf-8"), "data":message['data'].decode('utf-8')})
				else:
					yield 'data: %s\n\n' % message["data"]
	finally:
		user.online = 0
		db.session.commit()
		print("CLOSED", user.username)
		# TODO handle logout

# alternatively, save last request timestamp of user, assume offline? - doesn't really work if on same page -> but could add this mechanism inside event_stream too

def getRequestOrTempUser():
	user = getRequestUser()
	if user is not None:
		return True, user
	else:
		#print(request.args)
		tmpid = request.args.get("tmpid")
		user = User(username=tmpid)
		return False, user

@jwt_required
@app.route('/stream')
def stream():
	real, user = getRequestOrTempUser()
	return Response(event_stream(user),
						  mimetype="text/event-stream")

import os
if __name__ == "__main__":
	"""
	if os.getcwd().startswith("/root"):
		app.run("0.0.0.0", threaded=True, ssl_context=("/etc/letsencrypt/live/qewasd.com/cert.pem", "/etc/letsencrypt/live/qewasd.com/privkey.pem"))
	else:
		app.run("0.0.0.0", threaded=True)
	"""
	app.run("0.0.0.0", port=10000, threaded=True)
