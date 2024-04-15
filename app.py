# Exercise
# Create a web application with login and register 
# functionality for users to register and log in. 
# The register page should feature an HTML form with email 
# and password fields, while the login page should utilize a 
# Flask WTF form with email and password fields. Upon 
# successful registration, display "Successful registration". 
# Upon successful login, display "Logged in successfully". On 
# login failure, display "Incorrect email or password".

# Define User Database Model: 
# Create a User database model with the following attributes:
# id: Primary key 
# email: Unique and not nullable string 
# password: Not nullable string 

# Create Register Page:
# Define a route "/register" for the register page. 
# Implement a function to handle GET and POST requests. 
# On GET request, render the register template (register form).
# On POST request, handle registration form data.
# If registration is successful, return "Successful registration!" text.

# Create Register HTML Template:
# Create a "register.html" template.
# Design the template to include a register form with:
# Email field
# Password field
# Submit button

# Create Login Page:
# Define a route "/login" for the login page.
# Implement a function to handle GET and POST requests.
# On GET request, render the login template (login form).
# On POST request, handle login form data.
# If login is successful, return "Logged in successfully" text.
# If login fails, return "Invalid email or password" text. 
# (Check if user with provided email and password exists)

# Create Login HTML Template:
# Create a "login.html" template.
# Design the template to include a login form with:
# Email field
# Password field
# Submit button

# Utilize Flask-WTF for Login Form:
# Create a Flask WTF form for the login page.
# Include email and password fields with required validations.
# Implement Login Form Validations:
# Ensure that the email field has email and required validations.
# Ensure that the password field has a required validation.

from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = '125sddf89656'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return 'Successful registration!'
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            return 'Logged in successfully!'
        else:
            return 'Invalid email or password!'
    return render_template('login.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)