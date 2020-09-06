from flask import Blueprint,flash,render_template,redirect,request,url_for
from flaskblog import db,bcrypt
from flaskblog.users.forms import RegistrationForm,LoginForm,UpdateAccountForm,SendResetForm,PasswordResetForm
from flask_login import current_user,login_required,login_user,logout_user
from flaskblog.models import Post,User
from flaskblog.users.utils import save_picture, send_email

users = Blueprint('users',__name__)


@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('You have been succesfully registered! Log in!','success')
        return redirect(url_for('users.login'))
    return render_template('register.html',form=form,legend='Join us now!',title='Register')

@users.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            flash(f'Hello {user.username}! You are successfuly loged in','success')
            return redirect(url_for('main.home'))
        else:
            flash('Wrong credentials!', 'danger')

    return render_template('login.html',form=form,legend='Log in',title='Register')

@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been loged out','info')
    return redirect(url_for('main.home'))

@users.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.img_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account has been updated','success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    img_file = url_for('static',filename = 'profile_pics/'+current_user.img_file)
    return render_template('account.html',form=form,legend='Account info',title='Account',img_file=img_file)


@users.route('/password/send_reset_token',methods=['GET','POST'])
def send_reset_token():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SendResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_email(user)
            flash('Reset passwords has been sent please. Please follow instructions','info')
            return redirect(url_for('users.login'))
        else:
            flash('There is no such email registered. Please retry','danger')
            return redirect(url_for('users.send_reset_token'))
    return render_template('send_reset_token.html',form=form,legend='Send Reset Token',title='Send Reset')

@users.route('/password/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_token(token)
    if not user:
        flash('That is an invalid token','warning')
        return redirect(url_for('users.send_reset_token'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Password is changed. Please login', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_password.html',form=form,legend='Send Reset Token',title='Send Reset')