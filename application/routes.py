from flask import render_template,redirect, url_for, request
from application import app, db
from application.models import *
from application.forms import PostForm, RegistrationForm, LoginForm, UpdateAccountForm, TeamForm, DeleteAccount
from application import app,db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import requests

@app.route('/')
@app.route('/home')
def home():
    postData = Posts.query.all()
    return render_template('home.html', title = 'home', posts=postData)

# @app.route('/teams')
# @login_required
# def teams():
#     form = TeamForm()
#     if form.validate_on_submit():
#         postData = Posts(
#             title=form.title.data,
#             content=form.content.data,
#             author=current_user)
#         db.session.add(postData)
#         db.session.commit()
#         return redirect(url_for('teams'))

#     else:
#         print(form.errors)

#     return render_template('teams.html', title='Create Team',form=form)


# TODO change this
#   return "default until i sort something lol... navigate to ^^^^/about pls"

@app.route('/about')
def about():
    return render_template('about.html', title = 'About')

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))

    return render_template('login.html', title = 'Login',form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        user = Users(
            first_name=form.first_name.data, 
            last_name=form.last_name.data,
            email=form.email.data,
            password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('post'))
    return render_template('register.html', title = 'Register', form=form)

@app.route('/post', methods=['GET','POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        postData = Posts(
            title=form.title.data,
            content=form.content.data,
            author=current_user)
        db.session.add(postData)
        db.session.commit()
        return redirect(url_for('home'))

    else:
        print(form.errors)
    return render_template('post.html',
    title='Post', form=form)

@app.route('/update_account', methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    return render_template('update_account.html', title='Update Details', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email

    return render_template('account.html', title='Account', form=form)

@app.route('/delete_account', methods=['GET','POST'])
def delete_account():
    user_id = current_user.id
    user = Users.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('register'))
