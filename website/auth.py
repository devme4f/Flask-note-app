from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')

		user = User.query.filter_by(email=email).first()
		if user:
			if check_password_hash(user.password, password):
				flash('Login successfully!', category='success')
				login_user(user, remember=True) # flask sessions
				return redirect(url_for('views.home'))
			else:
				flash('Incorrent password, please try again!', category='error')
		else:
			flash('Email does not exists!')

	return render_template("login.html", user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		email = request.form.get('email')
		firstName = request.form.get('firstName')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')

		user = User.query.filter_by(email=email).first()
		if user:
			flash('Email already exists!', category='error')
		elif len(email) < 4:
			flash('Email must be greater than 4 characters.', category='error')
		elif len(firstName) < 3:
			flash('First name must be greater than 3 characters', category='error')
		elif len(password1) < 7:
			flash('Password must greater than 7 characters', category='error')
		elif password1 != password2:
			flash('Password does not match', category='error')
		else:
			new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'))
			db.session.add(new_user)
			db.session.commit()
			flash('Account created!', category='success')
			user = User.query.filter_by(email=email).first()
			login_user(user, remember=True)
			return redirect(url_for('views.home')) # redirect('/')

	return render_template("sign_up.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))