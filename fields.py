import re
from dao.db import *
from dao.orm.model import *
from sqlalchemy.exc import DatabaseError

customAttribute = r'\\template{(.*?)}'


def parseTemplateFields(text, template_id):
    for m in re.finditer(customAttribute, text):
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

def getTemplateFields(template_id):
    db = PostgresDb()

    return db.sqlalchemy_session.query(Fields).filter(Fields.template_id == template_id).all()