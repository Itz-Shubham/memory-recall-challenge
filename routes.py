from flask import Blueprint, render_template, session, redirect, request, send_file
from flask_login import login_required, login_user,logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
from datetime import datetime, timedelta
from models import db, User, PasswordResetToken
from fuctions import send_forget_password_mail

routes = Blueprint('route', __name__)

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('skipped_login'): session['skipped_login'] = False
        if current_user.is_authenticated: return redirect('/')
        return render_template('login.html')
    else:
        if request.form.get('skip-login'):
            session['skipped_login'] = True
            return redirect('/')
        
        email = request.form.get('email')
        password = request.form.get('password')

        error_messages = {}
        if not email: error_messages['email'] = "Enter a valid email"
        if not password: error_messages['password'] = "Enter a valid password"
        if len(password)<5: error_messages['password'] = "Password is too short. Please choose a password that is at least 6 characters long."
        if len(error_messages) != 0: return render_template('login.html', error_messages=error_messages)

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            error_messages['error'] = "Please check your login details and try again."
            return render_template('login.html', error_messages=error_messages)
        
        session['skipped_login'] = False
        login_user(user, remember=True)
        return redirect('/')

    
@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if session.get('skipped_login'): session['skipped_login'] = False
        if current_user.is_authenticated: return redirect('/')
        return render_template('register.html')
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        error_messages = {}

        if not name: error_messages['name'] = "Enter a valid name"
        if not email: error_messages['email'] = "Enter a valid email"
        if not password: error_messages['password'] = "Enter a valid password"
        if password and len(password)<5: error_messages['password'] = "Password is too short. Please choose a password that is at least 6 characters long."

        user = User.query.filter_by(email=email).first()
        if user: error_messages['email'] = 'Email address already exists'

        if len(error_messages) != 0: return render_template('register.html', error_messages=error_messages)

        new_user = User(email=email, name=name, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return redirect('/')

@routes.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'GET':
        if current_user.is_authenticated: return redirect('/')
        return render_template('forget-password.html')
    else:
        email = request.form.get('email')
        if not email: 
            return render_template('forget-password.html', error_messages={'email': "Enter a valid email"})
        
        user = User.query.filter_by(email=email).first()
        if not user:
            return render_template('forget-password.html', error_messages={'error': "There is no user exist with this email"})
        
        password_reset_token = PasswordResetToken.query.filter_by(user_id=user.id).first()
        token = str(uuid4()).replace('-', '')[:32]
        if not password_reset_token:
            password_reset_token = PasswordResetToken(token=token, user_id=user.id)
        else:
            if (datetime.now() - password_reset_token.date) < timedelta(minutes=15):
                return render_template('forget-password.html', error_messages={'error': "Password reset link sent to your email. Please check your inbox, and spam folder if needed, to complete the process."})
            password_reset_token.token = token
            password_reset_token.date = datetime.now()
        db.session.add(password_reset_token)
        db.session.commit()

        email_sent = send_forget_password_mail(user.email, token)
        return render_template('forget-password.html', email_sent=email_sent)
        
@routes.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'GET':
        if current_user.is_authenticated or request.args.get('token'):
            return render_template('change-password.html')
        return redirect('/')
    else:
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if not password1 or len(password1) < 5:
            return render_template('change-password.html', error_messages={'error': "Password is too short. Please choose a password that is at least 6 characters long."})
        if password1 != password2:
            return render_template('change-password.html', error_messages={'error': "Password doesn't matched"})
        if current_user.is_authenticated:
            current_user.password = generate_password_hash(password1)
            db.session.commit()
            return render_template('change-password.html', password_updated=True)
        else:
            token = request.args.get('token')
            password_reset_token = PasswordResetToken.query.filter_by(token=token).first()
            if not password_reset_token:
                return render_template('change-password.html', error_messages={'error': "Invalid Token!"})
            if (datetime.now() - password_reset_token.date) >= timedelta(hours=24):
                return render_template('change-password.html', error_messages={'error': "Password Reset Token is expired!"})
            user = User.query.filter_by(id=password_reset_token.user_id).first()
            user.password = generate_password_hash(password1)
            db.session.delete(password_reset_token)
            db.session.commit()
            return redirect('/login')


@routes.route('/logout')
def logout():
    logout_user()
    if session.get('skipped_login'): session.clear()
    return redirect('/')

@routes.route('/')
@routes.route('/home')
def index():
    users = User.query.order_by(User.high_score.desc()).all()
    if current_user.is_authenticated or session.get('skipped_login'):
        position = None
        if current_user.is_authenticated:
            position = users.index(current_user)
        top3users = None
        if len(users) > 3:
            top3users = users[:3]
            users = users[3:]
        print(top3users)
        return render_template('index.html', top3users=top3users, users=users, position=position)
    else:
        return redirect('/login')    

@login_required
@routes.route('/profile', methods=['GET', 'POST'])
def profile():
    if not current_user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        return render_template('profile.html')
    else:
        if 'profile_picture' in request.files and request.files['profile_picture']:
            photo = request.files['profile_picture']
            photo_path = f'uploads/profiles/user_{current_user.id}.{photo.filename.split(".")[-1]}'
            photo.save(photo_path)
            current_user.profile_picture = '/' + photo_path
        
        name = request.form.get('name')
        if name:
            current_user.name = name
            if len(name) < 3:
                return render_template('profile.html', error_messages={'name': 'Enter a valid name'})
        email = request.form.get('email')
        if email:
            current_user.email = email
            if len(email) < 10:
                return render_template('profile.html', error_messages={'email': 'Enter a valid email'})

        db.session.add(current_user)
        db.session.commit()
        return render_template('profile.html')


@routes.route('/about')
def about():
    return render_template('about.html')

@routes.route('/contact')
def contact():
    return render_template('contact.html')

from os.path import join as join_path
@routes.route('/uploads/profiles/<file_name>')
def download_file(file_name):
    return send_file(join_path('uploads/profiles/', file_name))
