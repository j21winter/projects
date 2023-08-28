from app import app
from app.models.user_model import User
from flask import render_template, jsonify, request, redirect, flash, session
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

@app.route('/')
def index():
    # User.data_upload()
    return redirect('/home')

@app.route('/home')
def login():
    return render_template('user_login.html')

@app.route('/user/register', methods=['POST'])
def register_user():
    print(request.form['email'])
    # validate info
    if not User.validate_user(request.form):
        flash('registration unsuccessful')
        return redirect("/")
    
    # save user & add user to session
    session['name'] = request.form['name']
    session['id'] = User.create_user(
        {
            'name': request.form['name'],
            'email': request.form['email'],
            'password': request.form['password']
            })
    
    # redirect to dashboard
    return redirect('/user/dashboard')

@app.route('/user/login', methods=['POST'])
def login_user():

    # search user by their email
    user = User.get_user_with_email(request.form['email'])

    # validate email exists in the DB 
        # if false redirect back to ("/')
    if not user:
        flash('INVALID LOGIN CREDENTIALS', 'login')
        return redirect('/user/logout')
    
    # compare hash password input to the stored hash password
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('INVALID password CREDENTIALS', 'login')
        return redirect('/user/logout')
    
    # if match is true then add user to session and redirect to dashboard
    session['id'] = user.id
    session['name'] = user.name

    return redirect('/user/dashboard')

@app.route('/user/logout')
def logout():
    session.clear()
    
    return redirect('/')

@app.route('/user/dashboard')
def dashboard():
    return render_template('user_dashboard.html', user = User.get_user_by_id(session['id']))