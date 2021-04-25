from flask import Blueprint, render_template ,session,request,current_app
from flask_login import login_required, current_user
from .models import User

from . import db
main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        u = User.query.filter_by(name=current_user.name).first()
    return render_template('articles.html')

def checkfree(articlename):
    
    #if user has logged in /  has an account
    if current_user.is_authenticated:
        u = User.query.filter_by(name=current_user.name).first()
        if u.free > 0:
            if articlename in str(u.freearticles):
                session['allow']= True
                return u.free
            else:
                u.free-=1
                if u.freearticles is None :
                    print("u.freearticles none",u.freearticles)
                    u.freearticles=articlename
                else:
                    print("u.freearticles there",u.freearticles)
                    u.freearticles+=articlename
                db.session.commit()
                session['allow']= True
                return u.free
        else:
            if articlename in str(u.freearticles):
                print("Free articles",u.freearticles)
                session['allow']= True
                return u.free
            else:
                session['allow']= False
                return u.free

    else: #if user hasn't logged in / no account
        if session.get('freeleft') is None: #first time viewing site without account
            session['freeleft'] = 3
            session['freeleft']-=1
            session['freeart']=articlename
            print("Your free articles:",session.get('freeart'))
            session['allow']= True
            return session['freeleft']
        elif session.get('freeleft') >0: # already viewed without account and free articles left
            if articlename not in session['freeart']:    #if viewer hasn't viewed the article before
                session['freeleft'] -=1
                session['freeart']+=articlename
                print("Your free articles:",session.get('freeart'))
                session['allow']= True
            else:
                print("Your free articles:",session.get('freeart'))
                session['allow']= True
            return session['freeleft']
        else: # no more free articles left
            if articlename not in session['freeart']:
                print("No free articles left")
                session['allow']= False
                return session['freeleft']
            else:
                session['allow']= True
                return session['freeleft']

@main.route('/article1')
def article1():
    f=checkfree("art1.")
    print("Free Articles left:",f)
    return render_template('a1.html',free=f)
    

@main.route('/article2')
def article2():
    f=checkfree("art2.")
    print("Free Articles left:",f)
    return render_template('a2.html',free=f)

@main.route('/article3')
def article3():
    f=checkfree("art3.")
    print("Free Articles left:",f)
    return render_template('a3.html',free=f)

@main.route('/article4')
def article4():
    f=checkfree("art4.")
    print("Free Articles left:",f)
    return render_template('a4.html',free=f)

@main.route('/article5')
def article5():
    f=checkfree("art5.")
    print("Free Articles left:",f)
    return render_template('a5.html',free=f)

@main.route('/article6')
def article6():
    f=checkfree("art6.")
    print("Free Articles left:",f)
    return render_template('a6.html',free=f)


