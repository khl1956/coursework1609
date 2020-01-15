import json
import hashlib
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from dao.orm.model import *
from dao.credentials import *
from dao.db import PostgresDb
from flask_app import *

Base = declarative_base()

app = Flask(__name__)

from login import *
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
#clearSessions()


@app.route('/', methods=['GET', 'POST'])
def root():
    sessionId = getUserSessionId(request)
    userLoggedIn = isUserLoggedIn(sessionId)

    return render_template('index.html', isUserLoggedIn=userLoggedIn)