
# IMPORT AND FROM #
import requests,click,wtforms

from peewee import *
from wtfpeewee.orm import model_form
from flask_wtf import FlaskForm
from flask import Flask, flash, redirect, render_template, request, url_for,session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from test.forms import *
from test.models import User,feed,create_tables,drop_tables,database



#----------------------------------#


# PARAMETERS #
app=Flask(__name__)
app.secret_key="root"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager._login_disabled = False


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get(user_id)
        print("ici fdp")
    except :
        return "va te faire enculer 2"
    
#------------------#

@app.route('/')
def index():
    if 'username' in session:
        flash(session['username'])
        return render_template('base.html')
    else:
        flash("Veuillez vous connecter")
        return redirect(url_for('signup'))
    return render_template('base.html')

@app.route('/nombre_user')
def dashboard():
    query=User.select()
    return render_template('user.html',query=query)


@app.route('/add_feed', methods=['GET', 'POST'])
@login_required
def add_feed():
    user_id = current_user.get_id() # return username in get_id()
    myfeed=feed()
    form=FeedForm()
    form.user_feed=user_id
    if form.validate_on_submit():
        form.populate_obj(myfeed)
        myfeed.save()
        flash('Your feed is save !!')
        return redirect(url_for('index'))
    return render_template('index.html',form=form)




@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print('ici')
    if form.validate_on_submit():
        try:
            user =User.get(User.user_username == form.username.data)
            if user.user_password==form.password.data:
                user.is_authenticated = True
                login_user(user)
                session['username'] = request.form['username']
                flash("You're now logged in!")
                return redirect(url_for('index'))
            else:
                flash("Error on password or username")
        except:
            flash("Error !!,You should start again")
    return render_template('login.html', form=form)
    


@app.route('/signup',methods=['GET','POST'])
def signup():
    user=User()
    form=UserForm()
    if form.validate_on_submit():
        form.populate_obj(user)
        user.save(force_insert=True)
        flash('Your account are been created')
        return redirect(url_for('dashboard'))
    return render_template('index.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    session.pop('username', None)
    return render_template('base.html')


@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return "Impossible !! You must first login to access it"

# FONCTIONS #

@app.cli.command()
def initdb():
    """Create database"""
    create_tables()
    click.echo('Initialized the database')

@app.cli.command()
def dropdb():
    """Drop database tables"""
    drop_tables()
    click.echo('Dropped tables from database')


if __name__=='__main__':
    app.run()
    app.debug = True