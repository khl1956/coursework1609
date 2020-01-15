import hashlib
import uuid

from flask import *
from sqlalchemy.exc import DatabaseError

from dao.db import *
from dao.orm.model import *
from flask_app import *
from forms.login_form import LoginForm
from forms.register_form import RegisterForm

session_id_key = 'session_id'


def getUserSessionId(request):
    return request.cookies.get(session_id_key)


def isUserLoggedIn(session_id):
    db = PostgresDb()
    response = db.sqlalchemy_session.query(UserSessions).filter(UserSessions.session_id == session_id).all()

    return len(response) != 0


def getLoggedUser(session_id):
    db = PostgresDb()
    response = db.sqlalchemy_session.query(UserSessions).filter(UserSessions.session_id == session_id).all()

    return response[0] if len(response) != 0 else None


@app.route('/login', methods=['GET', 'POST'])
def login():
    loggedInUser = getLoggedUser(getUserSessionId(request))
    if loggedInUser != None:
        return redirect('/')

    form = LoginForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('login_form.html', isUserLoggedIn=False, form=form, form_name="Login",
                                   action="login", method='POST')
        else:
            username = form.username.data
            password_hash = getPasswordHash(form.password.data)

            db = PostgresDb()

            response = db.sqlalchemy_session.query(Users).filter(Users.username == username).filter(
                Users.password_hash == password_hash).all()

            if len(response) != 1:
                return render_template('login_form.html', isUserLoggedIn=False, form=form, form_name="Login",
                                       action="login", method='POST')

            user_id = response[0].user_id

            new_uuid = str(uuid.uuid4())
            new_session = UserSessions(user_id=user_id, session_id=new_uuid)

            db.sqlalchemy_session.add(new_session)
            try:
                db.sqlalchemy_session.commit()
            except DatabaseError as e:
                db.sqlalchemy_session.rollback()
                print(e)

            response = make_response(redirect('/'))
            response.set_cookie(session_id_key, new_uuid)
            return response

    return render_template('login_form.html', isUserLoggedIn=False, form=form, form_name="Login", action="login",
                           method='POST')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    loggedInUser = getLoggedUser(getUserSessionId(request))
    if loggedInUser == None:
        return redirect('/')

    session_id = getUserSessionId(request)
    response = make_response(redirect('/'))
    response.set_cookie(session_id_key, '', expires=0)

    db = PostgresDb()
    db.sqlalchemy_session.query(UserSessions).filter(UserSessions.session_id == session_id).delete()

    try:
        db.sqlalchemy_session.commit()
    except DatabaseError as e:
        db.sqlalchemy_session.rollback()
        print(e)

    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    loggedInUser = getLoggedUser(getUserSessionId(request))
    if loggedInUser != None:
        return redirect('/')

    form = RegisterForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('register_form.html', isUserLoggedIn=False, form=form, form_name="Register",
                                   action="register", method='POST')
        else:
            user = Users(password_hash=getPasswordHash(form.password.data), username=form.username.data,
                         email=form.email.data)

            db = PostgresDb()
            db.sqlalchemy_session.add(user)
            try:
                db.sqlalchemy_session.commit()
            except DatabaseError as e:
                db.sqlalchemy_session.rollback()
                print(e)

            return redirect('/')

    return render_template('register_form.html', isUserLoggedIn=False, form=form, form_name="Register",
                           action="register", method='POST')


def getPasswordHash(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
