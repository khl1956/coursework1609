import datetime
import os
import shutil
import subprocess
from shutil import copyfile

from fields import *
from login import *


def generateDocumentFromCurrentFieldState(template_id, document_name):
    db = PostgresDb()

    template = db.sqlalchemy_session.query(Templates).filter(Templates.template_id == template_id).one()

    user_id = template.user_id

    folder_name = '/AutoDocument/Documents/{}'.format(user_id)
    uid = uuid.uuid1()
    temp_folder_name = '/AutoDocument/Temp/{}'.format(uid)
    path = '{}/{}_{}.pdf'.format(folder_name, document_name, uuid.uuid1())
    temp_template_path = '{}/temp.tex'.format(temp_folder_name)
    temp_document_path = '{}/temp.pdf'.format(temp_folder_name)

    os.makedirs(folder_name, exist_ok=True)
    os.makedirs(temp_folder_name, exist_ok=True)

    template_text = getFilledTemplateText(template)
    with open(temp_template_path, 'w') as file:
        file.write(template_text)

    try:
        subprocess.check_call(['pdflatex', '-recorder', '-output-directory=' + os.path.abspath(temp_folder_name),
                               os.path.abspath(temp_template_path)], timeout=10)
        copyfile(temp_document_path, path)
    except Exception as e:
        print(e)
        raise
    finally:
        shutil.rmtree(temp_folder_name, ignore_errors=True)

    document = Documents(
        user_id=user_id,
        document_name=document_name,
        document_file_path=path,
        document_upload_date=datetime.date.today()
    )

    db = PostgresDb()
    db.sqlalchemy_session.add(document)
    try:
        db.sqlalchemy_session.commit()
    except DatabaseError as e:
        db.sqlalchemy_session.rollback()
        print(e)


@app.route('/documents', methods=['GET'])
def documents():
    db = PostgresDb()

    loggedInUser = getLoggedUser(getUserSessionId(request))
    if loggedInUser == None:
        return redirect('/')

    result = db.sqlalchemy_session.query(Documents).filter(Documents.user_id == loggedInUser.user_id).all()
    return render_template('documents.html', isUserLoggedIn=True, documents=result)


@app.route('/delete_document', methods=['POST'])
def delete_document():
    loggedInUser = getLoggedUser(getUserSessionId(request))
    if loggedInUser == None:
        return redirect('/')

    document_id = request.form['document_id']

    db = PostgresDb()

    document = documentById(document_id)

    db.sqlalchemy_session.delete(document)
    try:
        db.sqlalchemy_session.commit()

        os.remove(document.document_file_path)
    except DatabaseError as e:
        db.sqlalchemy_session.rollback()
        print(e)
        return redirect('/documents')

    return redirect('/documents')


@app.route('/download_document', methods=['GET'])
def download_document():
    loggedInUser = getLoggedUser(getUserSessionId(request))
    if loggedInUser == None:
        return redirect('/')

    document_id = request.args.get('document_id')
    document = documentById(document_id)

    return send_file(document.document_file_path)


def documentById(document_id):
    db = PostgresDb()
    return db.sqlalchemy_session.query(Documents).filter(Documents.document_id == document_id).one()
