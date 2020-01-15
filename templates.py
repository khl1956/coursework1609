import datetime
import hashlib
import os
import uuid

from flask import *
from sqlalchemy.exc import DatabaseError
from werkzeug.utils import secure_filename

from documents import generateDocumentFromCurrentFieldState
from flask_app import *

from dao.db import *
from dao.orm.model import *
from forms.add_templates_form import *
from forms.generate_templates_form import GenerateTemplatesForm, FieldForm

from login import *
from fields import *


@app.route('/templates', methods=['GET'])
def templates():
    db = PostgresDb()

    loggedInUser = getLoggedUser(getUserSessionId(request))
    if loggedInUser == None:
        return redirect('/')

    result = db.sqlalchemy_session.query(Templates).filter(Templates.user_id == loggedInUser.user_id).all()
    return render_template('templates.html', isUserLoggedIn=True, templates=result)


@app.route('/new_template', methods=['GET', 'POST'])
def new_template():
    loggedInUser = getLoggedUser(getUserSessionId(request))
    if loggedInUser == None:
        return redirect('/')

    form = AddTemplatesForm()

    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('add_templates_form.html', isUserLoggedIn=True, form=form, form_name="New template",
                                   action="new_template",
                                   method='POST')
        else:
            name = form.template_name.data
            user_id = loggedInUser.user_id
            folder_name = '/AutoDocument/Templates/{}'.format(user_id)
            path = '{}/{}_{}.tex'.format(folder_name, name, uuid.uuid1())

            os.makedirs(folder_name, exist_ok=True)

            bytes = form.file.data.read()

            file = open(path, "wb")
            file.write(bytes)
            file.close()

            text = bytes.decode('utf-8')

            template = Templates(
                user_id=user_id,
                template_name=name,
                template_file_path=path,
                template_upload_date=datetime.date.today()
            )

            db = PostgresDb()
            db.sqlalchemy_session.add(template)
            try:
                db.sqlalchemy_session.commit()
                parseTemplateFields(text, template.template_id)
            except DatabaseError as e:
                db.sqlalchemy_session.rollback()
                print(e)
                return redirect('/templates')

            return redirect('/templates')

    return render_template('add_templates_form.html', isUserLoggedIn=True, form=form, form_name="New template",
                           action="new_template")


@app.route('/generate_template', methods=['GET', 'POST'])
def generate_template():
    loggedInUser = getLoggedUser(getUserSessionId(request))
    if loggedInUser == None:
        return redirect('/')

    template_id = request.args.get('template_id')

    form = generateEditTemplateForm(template_id)

    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('generate_templates_form.html', isUserLoggedIn=True, form=form,
                                   form_name="Edit template", action="generate_template?template_id=" + request.args.get('template_id'), method='POST')
        else:
            updateFields(form.fields.data, template_id)

            document_name = form.document_name.data

            db = PostgresDb()
            try:
                db.sqlalchemy_session.commit()

                generateDocumentFromCurrentFieldState(template_id, document_name)
            except Exception as e:
                db.sqlalchemy_session.rollback()
                print(e)
                return redirect('/templates')

            return redirect('/documents')

    return render_template('generate_templates_form.html', isUserLoggedIn=True, form=form,
                           form_name="Generate document",
                           action="generate_template?template_id=" + request.args.get('template_id'))


def generateEditTemplateForm(template_id):
    templateFields = getTemplateFields(template_id)

    formFields = []
    for field in templateFields:
        formFields.append({'content': field.field_content, 'nameData': field.field_name, 'id': field.field_id})

    return GenerateTemplatesForm(fields=formFields)


def updateFields(data, template_id):
    db = PostgresDb()

    for fieldData in data:
        id = fieldData['id']

        dbField = db.sqlalchemy_session.query(Fields).filter(Fields.field_id == id).filter(Fields.template_id == template_id).one()

        dbField.field_content = fieldData['content']


@app.route('/delete_template', methods=['POST'])
def delete_template():
    loggedInUser = getLoggedUser(getUserSessionId(request))
    if loggedInUser == None:
        return redirect('/')

    template_id = request.form['template_id']

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Templates).filter(Templates.template_id == template_id).one()

    db.sqlalchemy_session.delete(result)
    try:
        db.sqlalchemy_session.commit()

        os.remove(result.template_file_path)
    except DatabaseError as e:
        db.sqlalchemy_session.rollback()
        print(e)
        return redirect('/templates')

    return redirect('/templates')
