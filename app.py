from flask import Flask, render_template, json, url_for, request, redirect, jsonify, make_response
from flask.ext.login import LoginManager
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import logging
import redis
import uuid

# INIT

app = Flask(__name__)
app.secret_key = 'super secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dev:123456@mysql-server:3306/black_bill' #TODO should be in env file
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

r_server = redis.Redis('redis-server')

# MODELS

class User(db.Model):
	__tablename__ = "users"
	id = db.Column('user_id',db.Integer , primary_key=True)
	username = db.Column('user_name', db.String(20), unique=True , index=True)
	password = db.Column('password' , db.String(10))
	usertype = db.Column('user_type' , db.String(10))
	userstate = db.Column('user_state' , db.Integer)
	registered_on = db.Column('registered_on' , db.DateTime)
 
	def __init__(self , username ,password, usertype, userstate):
		self.username = username
		self.password = password
		self.usertype = usertype
		self.userstate = userstate
		self.registered_on = datetime.datetime.utcnow()

	def is_authenticated(self):
		return True
 
	def is_active(self):
		return True
 
	def is_anonymous(self):
		return False
 
	def get_id(self):
		return unicode(self.id)
 
	def __repr__(self):
		return '<User %r>' % (self.username)

class ObjectA(db.Model):
	__tablename__ = "objects_a"
	id = db.Column('objecta_id',db.Integer , primary_key=True)
	owner_id = db.Column('owner_id', db.Integer)
	session_id = db.Column('session_id', db.String(36))
	registered_on = db.Column('registered_on' , db.DateTime)
 
	def __init__(self, owner_id, session_id):
		self.owner_id = owner_id
		self.session_id = session_id
		self.registered_on = datetime.datetime.utcnow()

class ObjectB(db.Model):
	__tablename__ = "objects_b"
	id = db.Column('objecta_id',db.Integer , primary_key=True)
	owner_id = db.Column('owner_id', db.Integer)
	session_id = db.Column('session_id', db.String(36))
	registered_on = db.Column('registered_on' , db.DateTime)
 
	def __init__(self, owner_id, session_id):
		self.owner_id = owner_id
		self.session_id = session_id
		self.registered_on = datetime.datetime.utcnow()

class ObjectC(db.Model):
	__tablename__ = "objects_c"
	id = db.Column('objecta_id',db.Integer , primary_key=True)
	owner_id = db.Column('owner_id', db.Integer)
	session_id = db.Column('session_id', db.String(36))
	registered_on = db.Column('registered_on' , db.DateTime)
 
	def __init__(self, owner_id, session_id):
		self.owner_id = owner_id
		self.session_id = session_id
		self.registered_on = datetime.datetime.utcnow()

class ObjectD(db.Model):
	__tablename__ = "objects_d"
	id = db.Column('objecta_id',db.Integer , primary_key=True)
	owner_id = db.Column('owner_id', db.Integer)
	session_id = db.Column('session_id', db.String(36))
	registered_on = db.Column('registered_on' , db.DateTime)
 
	def __init__(self, owner_id, session_id):
		self.owner_id = owner_id
		self.session_id = session_id
		self.registered_on = datetime.datetime.utcnow()

class ObjectR(db.Model):
	__tablename__ = "objects_r"
	id = db.Column('objecta_id',db.Integer , primary_key=True)
	owner_id = db.Column('owner_id', db.Integer)
	foo = db.Column('foo', db.Integer)
	session_id = db.Column('session_id', db.String(36))
	registered_on = db.Column('registered_on' , db.DateTime)
 
	def __init__(self, owner_id, session_id, foo):
		self.owner_id = owner_id
		self.session_id = session_id
		self.foo = foo
		self.registered_on = datetime.datetime.utcnow()

db.create_all()
db.session.commit()

# API ENDPOINT

@app.route("/")
@app.route("/main")
def main():
	# assumption for simplicity - everyone would be on this page at least once (to gat session_id)
	session_id = request.cookies.get('session_id')
	status = r_server.get(session_id) # this is a bit redundunt, because no session espiration

	if not session_id or status != 'true':
		session_id = uuid.uuid4()
		r_server.set(session_id, 'true')
	resp = make_response(render_template('index.html'))
	resp.set_cookie('session_id', bytes(session_id))
	return resp

@app.route('/signup',methods=['GET','POST'])
def signUp():
	if request.method == 'GET':
		return render_template('signup.html')
	user = User(request.form['username'], request.form['password'], "user", 0)
	db.session.add(user)
	db.session.commit()
	return redirect(url_for('signin'))

@app.route('/signin',methods=['GET','POST'])
def signin():
	if request.method == 'GET':
		return render_template('signin.html')
	username = request.form['username']
	password = request.form['password']
	registered_user = User.query.filter_by(username=username,password=password).first()
	if registered_user is None:
		return redirect(url_for('signin'))
	login_user(registered_user)

	s_id = request.cookies.get('session_id')
	
	objectA = ObjectA.query.filter_by(session_id=s_id, owner_id=registered_user.id).first()
	if not objectA:
		objectA = ObjectA.query.filter_by(session_id=s_id).order_by(ObjectA.registered_on.desc()).first()	
		if objectA and objectA.owner_id == 0 and registered_user.userstate == 0:
			objectA.owner_id = registered_user.id
			registered_user.userstate = 1
			db.session.commit()

	return redirect(url_for('dashboard'))

@app.route('/signout')
def logout():
	logout_user()
	return redirect(url_for('main'))

@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
	if request.method == 'GET':
		return render_template('dashboard.html')
	return render_template('dashboard.html')

# BUSINESS LOGIC

@app.route('/mainCreateA',methods=['POST'])
def mainCreateA():
	owner_id = 0
	session_id = request.cookies.get('session_id')
	objectA = ObjectA(owner_id, str(session_id))
	db.session.add(objectA)
	db.session.commit()
	return jsonify({
		'objectA': {
			'id': objectA.id, 
			'session_id': session_id, 
			'owner_id': owner_id, 
			'timestamp': objectA.registered_on
		}
	})

# newxt three functions obviously have a lot in common and should be combined in one
@app.route('/dashboardCreateA',methods=['POST'])
@login_required
def dashboardCreateA():
	# Not sure if user can create multiple objectA after registration if yes
	# it is not really clear how it is different from just deleting objects
	if current_user.userstate > 0:
		return jsonify({'status': "objectA already assigned to this user"})
	else:
		s_id = request.cookies.get('session_id')
		objectA = ObjectA(current_user.id, str(s_id))
		db.session.add(objectA)
		current_user.userstate = 1
		db.session.commit()

		return jsonify({
			'objectA': {
				'id': objectA.id, 
				'session_id': objectA.session_id, 
				'owner_id': objectA.owner_id, 
				'timestamp': objectA.registered_on
			}
		})

@app.route('/dashboardCreateB',methods=['POST'])
@login_required
def dashboardCreateB():
	if current_user.userstate > 1:
		return jsonify({'status': "objectB already assigned to this user"})
	elif current_user.userstate < 1:
		return jsonify({'status': "You need to create objectA first"})
	else:
		s_id = request.cookies.get('session_id')
		objectB = ObjectB(current_user.id, str(s_id))
		db.session.add(objectB)
		current_user.userstate = 2
		db.session.commit()

		return jsonify({
				'objectB': {
				'id': objectB.id, 
				'session_id': objectB.session_id, 
				'owner_id': objectB.owner_id, 
				'timestamp': objectB.registered_on
			}
		})

@app.route('/dashboardCreateC',methods=['POST'])
@login_required
def dashboardCreateC():
	if current_user.userstate > 2:
		return jsonify({'status': "objectC already assigned to this user"})
	elif current_user.userstate < 2:
		return jsonify({'status': "You need to create objectA and objectB first"})
	else:
		s_id = request.cookies.get('session_id')
		objectC = ObjectC(current_user.id, str(s_id))
		db.session.add(objectC)
		current_user.userstate = 3
		db.session.commit()

		return jsonify({
				'objectC': {
				'id': objectC.id, 
				'session_id': objectC.session_id, 
				'owner_id': objectC.owner_id, 
				'timestamp': objectC.registered_on
			}
		})

@app.route('/dashboardCreateD',methods=['POST'])
@login_required
def dashboardCreateD():
	if current_user.userstate > 3:
		return jsonify({'status': "objectD already assigned to this user"})
	elif current_user.userstate < 3:
		return jsonify({'status': "You need to create objectA, objectB  and objectC first"})
	else:
		s_id = request.cookies.get('session_id')
		objectD = ObjectD(current_user.id, str(s_id))
		db.session.add(objectD)
		foo = randint(0,1)
		objectR = ObjectR(current_user.id, str(s_id), foo)
		db.session.add(objectR)
		current_user.userstate = 4
		db.session.commit()

		return jsonify({
			'objectD': {
				'id': objectD.id, 
				'session_id': objectD.session_id, 
				'owner_id': objectD.owner_id, 
				'timestamp': objectD.registered_on
			},
			'objectR': {
				'id': objectR.id, 
				'foo': objectR.foo,
				'session_id': objectR.session_id, 
				'owner_id': objectR.owner_id, 
				'timestamp': objectR.registered_on
			}
		})

@app.route('/showStatus',methods=['POST'])
@login_required
def showStatus():
	s_id = request.cookies.get('session_id')
	objectA = ObjectA.query.filter_by(session_id=s_id, owner_id=current_user.id).first()
	if current_user.userstate == 0:
		return jsonify({'status': "Not much happened yet"})
	elif current_user.userstate == 1:
		objectA = ObjectA.query.filter_by(session_id=s_id, owner_id=current_user.id).first()
		return jsonify({'objectA': objectA.id})
	elif current_user.userstate == 2:
		objectA = ObjectA.query.filter_by(session_id=s_id, owner_id=current_user.id).first()
		objectB = ObjectB.query.filter_by(session_id=s_id, owner_id=current_user.id).first()
		return jsonify({'objectA': objectA.id, 'objectB': objectB.id})
	elif current_user.userstate == 3:
		objectA = ObjectA.query.filter_by(session_id=s_id, owner_id=current_user.id).first()
		objectB = ObjectB.query.filter_by(session_id=s_id, owner_id=current_user.id).first()
		objectC = ObjectC.query.filter_by(session_id=s_id, owner_id=current_user.id).first()
		return jsonify({'objectA': objectA.id, 'objectB': objectB.id, 'objectC': objectC.id})
	elif current_user.userstate == 4:
		objectA = ObjectA.query.filter_by(session_id=s_id, owner_id=current_user.id).first()
		objectB = ObjectB.query.filter_by(session_id=s_id, owner_id=current_user.id).first()
		objectC = ObjectC.query.filter_by(session_id=s_id, owner_id=current_user.id).first()
		objectD = ObjectD.query.filter_by(session_id=s_id, owner_id=current_user.id).first()
		objectR = ObjectR.query.filter_by(session_id=s_id, owner_id=current_user.id).first()

		if objectR.foo == 0:
			current_user.userstate = 0
			db.session.delete(objectA)
			db.session.delete(objectB)
			db.session.delete(objectC)
			db.session.delete(objectD)
			db.session.delete(objectR)
		else:
			current_user.userstate = 5

		db.session.commit()

		return jsonify({'objectA': objectA.id, 
					'objectB': objectB.id, 
					'objectC': objectC.id, 
					'objectD': objectD.id, 
					'objectR.foo': objectR.foo
				})
	elif current_user.userstate == 5:
		return jsonify({'status': "Game over"})


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5000)
