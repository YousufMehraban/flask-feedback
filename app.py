from flask import Flask, redirect, render_template, session
from models import db, FeedbackUser as User, Feedback
from forms import UserForm, LoginForm, FeedbackForm
from flask_bcrypt import Bcrypt

app = Flask('hi')
bcrypt = Bcrypt()

app.config['SECRET_KEY'] = 'nothingsecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.app = app
db.init_app(app)


@app.route('/')
def index():
    """redirecting to register a user"""
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """registering a new user"""

    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        return redirect(f'/users/{username}')


    return render_template('register.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """if authenticated, login the user"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f'/users/{username}')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    """loging out the user"""

    session.pop('username')
    return redirect('/')


@app.route('/users/<username>')
def show_user(username):
    """showing details of a user"""

    if 'username' not in session:
        return redirect('/')

    user = User.query.get_or_404(username)
    feedbacks = Feedback.query.filter_by(username=user.username).all()
    return render_template('user.html', user=user, feedbacks=feedbacks)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """delete a user and all of thier feedbacks"""

    if 'username' in session:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.pop('username')

        return redirect('/')

    return redirect(f'/users/{username}')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """adding feedback"""
    
    if 'username' in session:
        form = FeedbackForm()

        if form.validate_on_submit():
                
            title = form.title.data
            content = form.content.data

            feedback = Feedback(title=title, content=content, username=username)
            db.session.add(feedback)
            db.session.commit()
            return redirect(f'/users/{username}')

        return render_template('add_feedback.html', form = form)

    return redirect('/')

@app.route('/feedback/<int:id>/update', methods=['GET', 'POST'])
def edit_feedback(id):
    """adding feedback"""
    
    if 'username' in session:

        feedback = Feedback.query.get_or_404(id)
        form = FeedbackForm(obj=feedback)

        if form.validate_on_submit():
                

            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            return redirect(f'/users/{feedback.user.username}')

        return render_template('edit_feedback.html', form = form)

    return redirect('/')

@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
    """delete a feedback"""
    
    if 'username' in session:

        feedback = Feedback.query.get_or_404(id)
        username = feedback.user.username
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')

    return redirect('/')
