import datetime
import hashlib
import uuid

from flask import *
from sqlalchemy.exc import DatabaseError

from flask_app import *

from dao.db import *
from dao.orm.model import *
from forms.fields_form import *


@app.route('/fields', methods=['GET'])
def fields():
    db = PostgresDb()

    result = db.sqlalchemy_session.query(Fields).all()
    return render_template('fields.html', fields=result)


@app.route('/new_field', methods=['GET', 'POST'])
def new_field():
    form = FieldsForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('fields_form.html', form=form, form_name="New field", action="new_field",
                                   method='POST')
        else:
            field = Fields(
                template_id=form.template_id.data,
                field_name=form.field_name.data,
                field_content=form.field_content.data,
            )

            db = PostgresDb()
            db.sqlalchemy_session.add(field)
            try:
                db.sqlalchemy_session.commit()
            except DatabaseError as e:
                db.sqlalchemy_session.rollback()
                print(e)
                return redirect('/fields')

            return redirect('/fields')

    return render_template('fields_form.html', form=form, form_name="New field", action="new_field")


@app.route('/edit_field', methods=['GET', 'POST'])
def edit_field():
    form = FieldsForm()

    if request.method == 'GET':

        field_id = request.args.get('field_id')
        db = PostgresDb()
        field = db.sqlalchemy_session.query(Fields).filter(Fields.field_id == field_id).one()

        form.template_id.data = field.template_id
        form.field_name.data = field.field_name
        form.field_content.data = field.field_content

        return render_template('fields_form.html', form=form, form_name="Edit field", action="edit_field?field_id=" + request.args.get('field_id'))
    else:
        if not form.validate():
            return render_template('fields_form.html', form=form, form_name="Edit field", action="edit_field?field_id=" + request.args.get('field_id'))
        else:
            db = PostgresDb()

            field = db.sqlalchemy_session.query(Fields).filter(Fields.field_id == request.args.get('field_id')).one()

            field.template_id = form.template_id.data
            field.field_name = form.field_name.data
            field.field_content = form.field_content.data

            try:
                db.sqlalchemy_session.commit()
            except DatabaseError as e:
                db.sqlalchemy_session.rollback()
                print(e)
                return redirect('/fields')

            return redirect('/fields')


@app.route('/delete_field', methods=['POST'])
def delete_field():
    field_id = request.form['field_id']

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Fields).filter(Fields.field_id == field_id).one()

    db.sqlalchemy_session.delete(result)
    try:
        db.sqlalchemy_session.commit()
    except DatabaseError as e:
        db.sqlalchemy_session.rollback()
        print(e)
        return redirect('/fields')

    return redirect('/fields')
