import hashlib

from flask import *
from sqlalchemy.exc import DatabaseError

from flask_app import *

from dao.db import *
from dao.orm.model import *
from forms.users_form import *


@app.route('/users', methods=['GET'])
def users():
    db = PostgresDb()

    result = db.sqlalchemy_session.query(Users).all()
    return render_template('users.html', users=result)


@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    form = UsersForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('users_form.html', form=form, form_name="New user", action="new_user",
                                   method='POST')
        else:
            user = Users(
                username=form.username.data,
                email=form.email.data,
                password_hash=hashlib.sha256(form.password.data.encode('utf-8')).hexdigest(),
            )

            db = PostgresDb()
            db.sqlalchemy_session.add(user)
            try:
                db.sqlalchemy_session.commit()
            except DatabaseError as e:
                db.sqlalchemy_session.rollback()
                print(e)
                return redirect('/users')

            return redirect('/users')

    return render_template('users_form.html', form=form, form_name="New user", action="new_user")


@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    form = UsersForm()

    if request.method == 'GET':

        user_id = request.args.get('user_id')
        db = PostgresDb()
        user = db.sqlalchemy_session.query(Users).filter(Users.user_id == user_id).one()

        form.username.data = user.username
        form.email.data = user.email
        form.password.data = ''

        return render_template('users_form.html', form=form, form_name="Edit user",
                               action="edit_user?user_id=" + request.args.get('user_id'))
    else:
        if not form.validate():
            return render_template('users_form.html', form=form, form_name="Edit user",
                                   action="edit_user?user_id=" + request.args.get('user_id'))
        else:
            db = PostgresDb()

            user = db.sqlalchemy_session.query(Users).filter(Users.user_id == request.args.get('user_id')).one()

            user.username = form.username.data
            user.email = form.email.data
            user.password_hash = hashlib.sha256(form.password.data.encode('utf-8')).hexdigest()

            try:
                db.sqlalchemy_session.commit()
            except DatabaseError as e:
                db.sqlalchemy_session.rollback()
                print(e)
                return redirect('/users')

            return redirect('/users')


@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form['user_id']

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Users).filter(Users.user_id == user_id).one()

    db.sqlalchemy_session.delete(result)
    try:
        db.sqlalchemy_session.commit()
    except DatabaseError as e:
        db.sqlalchemy_session.rollback()
        print(e)
        return redirect('/users')

    return redirect('/users')
