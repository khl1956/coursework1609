import datetime
import hashlib
import uuid

from flask import *
from sqlalchemy.exc import DatabaseError

from flask_app import *

from dao.db import *
from dao.orm.model import *
from forms.templates_form import *


@app.route('/templates', methods=['GET'])
def templates():
    db = PostgresDb()

    result = db.sqlalchemy_session.query(Templates).all()
    return render_template('templates.html', templates=result)


@app.route('/new_template', methods=['GET', 'POST'])
def new_template():
    form = TemplatesForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('templates_form.html', form=form, form_name="New template", action="new_template",
                                   method='POST')
        else:
            name = form.template_name.data
            user_id = form.user_id.data

            template = Templates(
                user_id=user_id,
                template_name=name,
                template_file_path='/{}/{}_{}.doc'.format(user_id, name, uuid.uuid1()),
                template_upload_date=datetime.date.today()
            )

            db = PostgresDb()
            db.sqlalchemy_session.add(template)
            try:
                db.sqlalchemy_session.commit()
            except DatabaseError as e:
                db.sqlalchemy_session.rollback()
                print(e)
                return redirect('/templates')

            return redirect('/templates')

    return render_template('templates_form.html', form=form, form_name="New template", action="new_template")


@app.route('/edit_template', methods=['GET', 'POST'])
def edit_template():
    form = TemplatesForm()

    if request.method == 'GET':

        template_id = request.args.get('template_id')
        db = PostgresDb()
        template = db.sqlalchemy_session.query(Templates).filter(Templates.template_id == template_id).one()

        form.user_id.data = template.user_id
        form.template_name.data = template.template_name

        return render_template('templates_form.html', form=form, form_name="Edit template",
                               action="edit_template?template_id=" + request.args.get('template_id'))
    else:
        if not form.validate():
            return render_template('templates_form.html', form=form, form_name="Edit template",
                                   action="edit_template?template_id=" + request.args.get('template_id'))
        else:
            db = PostgresDb()

            template = db.sqlalchemy_session.query(Templates).filter(Templates.template_id == request.args.get('template_id')).one()

            name = form.template_name.data
            user_id = form.user_id.data

            template.user_id = user_id,
            template.template_name = name,
            template.template_file_path = '/{}/{}_{}.doc'.format(user_id, name, uuid.uuid1()),
            template.template_upload_date = datetime.date.today()

            try:
                db.sqlalchemy_session.commit()
            except DatabaseError as e:
                db.sqlalchemy_session.rollback()
                print(e)
                return redirect('/templates')

            return redirect('/templates')


@app.route('/delete_template', methods=['POST'])
def delete_template():
    template_id = request.form['template_id']

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Templates).filter(Templates.template_id == template_id).one()

    db.sqlalchemy_session.delete(result)
    try:
        db.sqlalchemy_session.commit()
    except DatabaseError as e:
        db.sqlalchemy_session.rollback()
        print(e)
        return redirect('/templates')

    return redirect('/templates')
