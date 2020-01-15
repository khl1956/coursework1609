import re
from dao.db import *
from dao.orm.model import *
from sqlalchemy.exc import DatabaseError

customAttribute = r'\\template{%s}'


def parseTemplateFields(text, template_id):
    for m in re.finditer(customAttribute % '(.*?)', text):
        db = PostgresDb()

        fieldName = m.group(1)

        field = Fields(
            template_id=template_id,
            field_name=fieldName,
            field_content=''
        )

        db.sqlalchemy_session.add(field)
        try:
            db.sqlalchemy_session.commit()
        except DatabaseError as e:
            db.sqlalchemy_session.rollback()
            print(e)


def getFilledTemplateText(template):
    text = ''

    with open(template.template_file_path, 'r') as file:
        text = file.read()

    for field in getTemplateFields(template.template_id):
        text = re.sub(customAttribute % field.field_name, field.field_content, text, flags = re.M)

    return text

def getTemplateFields(template_id):
    db = PostgresDb()

    return db.sqlalchemy_session.query(Fields).filter(Fields.template_id == template_id).all()