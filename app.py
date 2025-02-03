from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
#for users
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin

# Initializing the app
app = Flask(__name__)
app.config.from_object('config.Config')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Initializing the database
db = SQLAlchemy(app)

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
    password = db.Column(db.String(150), nullable=False)

#creating database tables
with app.app_context():
    db.create_all()

## . ###

#route for Home Page
@app.route('/')
def home():
    return render_template('index.html')

#about page
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
        password = request.form['password'] # TO-DO : hash the password
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('your account has been created!', 'success')
        # using url_for to avoid hardcoding urls within the app's templates
        return redirect(url_for('login'))

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

        if user and user.password == password:
            login_user(user)
            # flash(message, category)
            flash('login Successfull!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Try Again.')

    return render_template('login.html')


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