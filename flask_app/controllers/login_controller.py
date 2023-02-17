from flask import render_template,request,redirect,session,flash
from flask_app import app
from flask_app import bcrypt
from flask_app.models.login_model import Users
from flask_app.models.band_model import Bands



@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/register_new_user',methods=['POST'])
def add_user():
    if not Users.validate_create(request.form):
        return redirect('/')
    if not request.form['password']:
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data={
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "email":request.form["email"],
        "password":pw_hash,
        "confirm_password":request.form["confirm_password"]
    }
    user = Users.get_by_email(request.form)
    if user:
        flash('User already exists in database')
        return redirect('/')
    else:
        Users.create_user(data)
    return redirect('/')

@app.route('/log_in',methods=['POST'])
def logging_in():
    data = {"email" : request.form["email"]}
    if not Users.validate_login(request.form):
        return redirect('/')
    user_in_db = Users.get_by_email(data)
    if user_in_db:
        if not bcrypt.check_password_hash(user_in_db.password,request.form['password']):
            flash('Invalid Email/Password')
            return redirect('/')
        session['email'] = user_in_db.email
        return redirect('/bands')
    else:
        flash('login invalid!')
        return redirect('/')



@app.route('/bands')
def logged_in():
    if 'email' in session:
        user = Users.dashboard_page({'email':session['email']})
        bands = Bands.show_all_bands()
        print(bands)
        session['id'] = user['id']
        return render_template('bands.html',user=user,bands=bands)
    else:
        flash('PLease enter an existing users information!')
        return redirect('/')

@app.route('/logging_out')
def logging_out():
    session.clear()
    return redirect('/')






@app.route('/dashboard')
def dashboard():
    return render_template('bands.html')