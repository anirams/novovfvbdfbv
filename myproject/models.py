from datetime import datetime
from myproject import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	izlet = db.relationship('Izlet', backref='author', lazy='dynamic') 
	prij = db.relationship('Izlet', secondary=prijava,
		primaryjoin=(prijava))

	def __repr__(self):
		return '<User {}>'.format(self.username)  

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
			digest, size)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class Izlet(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(140))
	description = db.Column(db.String(140))
	location = db.Column(db.String(140))
	transport = db.Column(db.String(70))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	begin = db.Column(db.Date, index=True)
	end = db.Column(db.Date, index=True)
	picture = db.Column(db.String(200))
	cost = db.Column(db.Numeric)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Izlet {}>'.format(self.body)

prijava = db.Table('prijava',
    db.Column('izlet_id', db.Integer, db.ForeignKey('izlet.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)