from dao.orm.model import *
from flask_app import *

Base = declarative_base()

app = Flask(__name__)

from templates import *


def clearSessions():
    db = PostgresDb()
    db.sqlalchemy_session.query(UserSessions).delete()

    try:
        db.sqlalchemy_session.commit()
    except DatabaseError as e:
        db.sqlalchemy_session.rollback()
        print(e)


db = PostgresDb()
Base.metadata.create_all(db.sqlalchemy_engine)


# clearSessions()


@app.route('/', methods=['GET', 'POST'])
def root():
    sessionId = getUserSessionId(request)
    userLoggedIn = isUserLoggedIn(sessionId)

    return render_template('index.html', isUserLoggedIn=userLoggedIn)
