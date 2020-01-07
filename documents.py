import datetime
import hashlib
import uuid

from flask import *
from sqlalchemy.exc import DatabaseError

from flask_app import *

from dao.db import *
from dao.orm.model import *
from forms.documents_form import *


@app.route('/documents', methods=['GET'])
def documents():
    db = PostgresDb()

    result = db.sqlalchemy_session.query(Documents).all()
    return render_template('documents.html', documents=result)


@app.route('/new_document', methods=['GET', 'POST'])
def new_document():
    form = DocumentsForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('documents_form.html', form=form, form_name="New document", action="new_document",
                                   method='POST')
        else:
            name = form.document_name.data
            user_id = form.user_id.data

            document = Documents(
                user_id=user_id,
                document_name=name,
                document_file_path='/{}/{}_{}.doc'.format(user_id, name, uuid.uuid1()),
                document_upload_date=datetime.date.today()
            )

            db = PostgresDb()
            db.sqlalchemy_session.add(document)
            try:
                db.sqlalchemy_session.commit()
            except DatabaseError as e:
                db.sqlalchemy_session.rollback()
                print(e)
                return redirect('/documents')

            return redirect('/documents')

    return render_template('documents_form.html', form=form, form_name="New document", action="new_document")


@app.route('/edit_document', methods=['GET', 'POST'])
def edit_document():
    form = DocumentsForm()

    if request.method == 'GET':

        document_id = request.args.get('document_id')
        db = PostgresDb()
        document = db.sqlalchemy_session.query(Documents).filter(Documents.document_id == document_id).one()

        form.user_id.data = document.user_id
        form.document_name.data = document.document_name

        return render_template('documents_form.html', form=form, form_name="Edit document",
                               action="edit_document?document_id=" + request.args.get('document_id'))
    else:
        if not form.validate():
            return render_template('documents_form.html', form=form, form_name="Edit document",
                                   action="edit_document?document_id=" + request.args.get('document_id'))
        else:
            db = PostgresDb()

            document = db.sqlalchemy_session.query(Documents).filter(Documents.document_id == request.args.get('document_id')).one()

            name = form.document_name.data
            user_id = form.user_id.data

            document.user_id = user_id,
            document.document_name = name,
            document.document_file_path = '/{}/{}_{}.doc'.format(user_id, name, uuid.uuid1()),
            document.document_upload_date = datetime.date.today()

            try:
                db.sqlalchemy_session.commit()
            except DatabaseError as e:
                db.sqlalchemy_session.rollback()
                print(e)
                return redirect('/documents')

            return redirect('/documents')


@app.route('/delete_document', methods=['POST'])
def delete_document():
    document_id = request.form['document_id']

    db = PostgresDb()

    result = db.sqlalchemy_session.query(Documents).filter(Documents.document_id == document_id).one()

    db.sqlalchemy_session.delete(result)
    try:
        db.sqlalchemy_session.commit()
    except DatabaseError as e:
        db.sqlalchemy_session.rollback()
        print(e)
        return redirect('/documents')

    return redirect('/documents')
