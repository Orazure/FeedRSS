
# IMPORT AND FROM #
import requests,click,wtforms

from peewee import *
from wtfpeewee.orm import model_form
from flask_wtf import FlaskForm
from flask import Flask, flash, redirect, render_template, request, url_for,session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from test.forms import *
from test.models import *
from flask_login import logout_user


#----------------------------------#


# PARAMETERS #
app=Flask(__name__)
app.secret_key="root"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager._login_disabled = False
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

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
    myfeed=feed()
    user_id = current_user.get_id() # return username in get_id()
    print("",user_id)
    form=FeedForm()
    form.user_feed=user_id
    if form.validate_on_submit():
        form.populate_obj(myfeed)
        myfeed.save()
        flash('Hooray ! Boardgame created !')
        return redirect(url_for('index'))
    return render_template('index.html',form=form)




@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user=User()
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)
        flash('Logged in successfully.')
        session['username'] = request.form['username']
        next = request.args.get('next')
        return redirect(next or url_for('index'))
    return render_template('login.html', form=form)
    

@app.route('/signup',methods=['GET','POST'])
def signup():
    user=User()
    form=UserForm()
    if form.validate_on_submit():
        form.populate_obj(user)
        user.save(force_insert=True)
        flash('Votre compte est crée')
        return redirect(url_for('dashboard'))
    return render_template('index.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    session.pop('username', None)
    return render_template('base.html')









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





@app.errorhandler(404)
def notfound():
    """Serve 404 template."""
    return make_response(render_template("404.html"), 404)

app.debug = True

if __name__=='__main__':
    app.run()