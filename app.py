from flask import Flask, render_template, url_for, redirect, request, flash
from models import * 
from extensions import db, migrate
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
#hashed passwords
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
#for users
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin

# Initializing the app
app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate.init_app(app, db) 

with app.app_context():
    db.create_all()

# Set the upload folder in app configuration
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

## User Setup ##
#Initializing LoginManager which connects the app with Flask Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'


#creating database tables
with app.app_context():
    db.create_all()

## . ###

# route for Home Page
@app.route('/')
def home():
    return render_template('index.html')

# about page
@app.route('/about')
def about():
    return render_template('about.html')

# route for Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Choose a different one.", "danger")
            return redirect(url_for('register'))

        # Create a new user and hash the password
        new_user = User(username=username)
        new_user.set_password(password)  # Store hashed password
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))  # Redirect to login page

    return render_template('register.html')

# Route for Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    #if the user is logged in successfully take them to home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            # flash(message, category)
            flash('login Successfull!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Try Again.', "danger")

    return render_template('login.html')

# User Profile
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    username = current_user.username
    return render_template('profile.html', user=current_user)

# Book Info Page
@app.route('/book-info', methods=["GET", "POST"])
@login_required
def book_info():
    # get the book from database
    return render_template("/book-info.html")


@app.route('/upload-profile-picture', methods=['POST'])
@login_required
def upload_profile_pic():
    # Check if the user submitted a file
    if 'profile_picture' not in request.files:
        flash('No file selected', 'danger')
        return redirect(url_for('profile'))

    file = request.files['profile_picture']
    # If the user doesn't select a file
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('profile'))
    
    if file and file.filename:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        current_user.profile_image = f'static/uploads/{filename}'
        db.session.commit()
        flash("Profile picture updated successfully!", "success")

    return redirect(url_for("profile"))

# Route for Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

# Initializing the User loader function for Flask-Login - a cookie kind of!
# used to define a function that tells Flask-Login how to load a user from the session based on their unique identifier (usually their user ID)
# This is crucial for maintaining a user’s logged-in session across different requests.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)