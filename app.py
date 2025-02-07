from flask import Flask, render_template, url_for, redirect, request, flash
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

# Set the upload folder in app configuration
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initializing the database
db = SQLAlchemy(app)
#Enabling Flask-Migrate
migrate = Migrate(app, db) 

## User Setup ##
#Initializing LoginManager which connects the app with Flask Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Defining User Model
# UserMixin is used as a helper class by Flask-Login to manage user sessions
# Adding UserMixin as parameter enables its use by the User model
# db.Model from flask_sqlalchemy is ubeing inherited by the user class that represents a database table
class User(UserMixin, db.Model):
    # main elements: id, username, password
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  # Store hashed password
    profile_image = db.Column(db.String(150), default='static/uploads/default_profile.jpg') 
    wallpaper_image = db.Column(db.String(150), default='static/uploads/default_wallpaper.jpg')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
        print("in if")
        filename=secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(filename)
        current_user.profile_image = f'uploads/{filename}'
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