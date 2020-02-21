import requests,click,wtforms,feedparser,random,logging

from base.feed import *
from log import *
from flask_restful import Resource, Api
from peewee import *
from wtfpeewee.orm import model_form
from flask_wtf import FlaskForm
from flask import Flask, flash, redirect, render_template, request, url_for,session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from base.forms import *
from base.models import User,feed,create_tables,drop_tables,database



# PARAMETERS #
app=Flask(__name__)
app.secret_key="root"
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get(user_id)
    except :
        return "Error account"
    
#------------------#

@app.route('/')
def index():
    if 'username' in session:
        flash(session['username'])
        return render_template('base.html')
    else:
        flash("Please ,you must to connecting")
        return redirect(url_for('signup'))
    return render_template('base.html')



@app.route('/feed/all_feed', methods=['GET', 'POST'])
@login_required
def All_feed():
    try:
        user_id = current_user.get_id() # return username in get_id()
    except Entry.DoesNotExist:
        abort(404)
    query=feed.select().where(feed.user_feed==user_id)
    dic={}
    liste_url=[key.feed_url for key in query]
    if(len(liste_url)>0):
        for _url in liste_url:  
            dic=feedparser.parse(_url).entries
            logger.debug("Feed (all) : %s")
    else:
        flash("You have not feed,created it")
        return redirect(url_for('index'))    
    return render_template("vue_all_feed.html",dic=dic,liste_feed_dic=feed_nom_url())

@app.route('/feed/<slug>', methods=['GET', 'POST'])
@login_required
def feed_nom(slug):
    try:
        user_id = current_user.get_id() # return username in get_id()
    except Entry.DoesNotExist:
        abort(404)
    query=feed.select(feed.feed_url).where(feed.user_feed==user_id,feed.feed_nom==slug)
    liste_url=[key.feed_url for key in query]
    if(len(liste_url)>0):
        for _url in liste_url:  
            dic=feedparser.parse(_url).entries
            logger.debug("c'est la merde %s")
    else:
        flash("Not found this feed")
        return render_template(url_for("All_feed"))
    return render_template("vue_all_feed.html",dic=dic,liste_feed_dic=feed_nom_url())



@app.route('/add_feed', methods=['GET', 'POST'])
@login_required
def add_feed():
    try:
        user_id = current_user.get_id() # return username in get_id()
    except Entry.DoesNotExist:
        abort(404)
    form=FeedForm()
    if form.validate_on_submit():
        myfeed=feed(
            feed_nom=form.feed_nom.data,
            feed_url=form.feed_url.data,
            feed_date=form.feed_date.data,
            user_feed=user_id)
        myfeed.save()
        flash('Your feed is save !!')
        return redirect(url_for('index'))
    return render_template('add_feed.html',form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user =User.get(User.user_username == form.username.data)
            if user.user_password==form.password.data:
                #user.is_authenticated = True
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
        return redirect(url_for('index'))
    return render_template('index.html', form=form)






def feed_nom_url():
    """
    retourne Url du feed
    """
    try:
        user_id = current_user.get_id() # return username in get_id()
    except Entry.DoesNotExist:
        abort(404)
    query=feed.select().where(feed.user_feed==user_id)
    liste_feed=[(key.feed_nom,key.feed_url) for key in query]
    liste_feed_dic=dict(liste_feed)
    return liste_feed_dic
   

@app.route('/logout')
def logout():
    logout_user()
    session.pop('username', None)
    return render_template('base.html')


@login_manager.unauthorized_handler
def unauthorized():
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
