from flask import render_template, request, flash, redirect, url_for
from myproject import app, db
from myproject.forms import StvoriIzletForm, LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from myproject.models import User, Izlet
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		#next_page = request.args.get('next')
		#if not next_page or url_parse(next_page).netloc != '':
		#	next_page = url_for('index')
		#return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))	
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('user.html', title='Profile', user=user)

@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/explore')
@login_required
def explore():
	page = request.args.get('page', 1, type=int)
	izleti = Izlet.query.order_by(Izlet.timestamp.desc()).paginate(
		page, app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('explore', page=izleti.next_num) \
		if izleti.has_next else None
	prev_url = url_for('explore', page=izleti.prev_num) \
		if izleti.has_prev else None
	return render_template("index.html", title='Explore', izleti=izleti.items,
                          next_url=next_url, prev_url=prev_url)

@app.route('/stvori_izlet', methods=['GET', 'POST'])
def stvori_izlet():	
	form = StvoriIzletForm()
	if form.validate_on_submit():
		izlet = Izlet(name=form.name.data, description=form.description.data, location=form.location.data, 
			transport=form.transport.data, begin=form.begin.data, end=form.end.data, 
			picture=form.picture.data, cost=form.cost.data, user_id=current_user.id)
		db.session.add(izlet)
		db.session.commit()
		flash('Dodali ste novi izlet!')
		return redirect(url_for('explore'))
	return render_template('stvori_izlet.html', title='Novi Izlet', form=form)