import plotly
import plotly.plotly as py
import plotly.graph_objs as go
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
from forms.dashboard_form import DashboardForm
from forms.users_form import *
from flask_app import *
from execute_sql_file import *


Base = declarative_base()

app = Flask(__name__)

from users import *
from documents import *
from templates import *
from fields import *

@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


# @app.route('/search', methods=['GET', 'POST'])
# def search():
#    search_form = SearchForm()
#
#    if request.method == 'GET':
#        return render_template('search.html', form=search_form, result=None)
#    else:
#        return render_template('search.html', form=search_form, result=search_form.get_result())


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    db = PostgresDb()

    form = DashboardForm()

    username = form.username.data

    template_fields = user_template_field_count(username)

    templates = []
    field_counts = []

    for (temp, field_count) in template_fields.items():
        templates.append(temp.template_name)
        field_counts.append(field_count)

    bar = go.Bar(
        x=templates,
        y=field_counts
    )

    dates = user_document_upload_date(username)

    x = []
    y = []

    for (date, document_count) in dates.items():
        x.append(date)
        y.append(document_count)

    scatter = go.Scatter(
        x=x,
        y=y,
    )

    data = [bar, scatter]

    ids = [0, 1]
    names = ["Template field count", "Field and templates count for each user"]
    graph_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('dashboard.html', form=form, form_name="Username", action="dashboard", username=username,
                           graphJSON=graph_json, ids=ids, names=names)


def user_template_field_count(username):
    db = PostgresDb()

    if not username:
        template_fields = db.sqlalchemy_session.query(Templates, Fields).join(Fields).all()
        temp = db.sqlalchemy_session.query(Templates).all()
    else:
        template_fields = db.sqlalchemy_session.query(Templates, Fields).join(Users).filter(
            Users.username == username).join(Fields).all()
        temp = db.sqlalchemy_session.query(Templates).join(Users).filter(Users.username == username).all()

    templates = {}

    for t in temp:
        templates[t] = 0

    for (template, field_count) in template_fields:
        key = template
        templates[key] += 1

    return templates


def user_document_upload_date(username):
    db = PostgresDb()

    if not username:
        documents = db.sqlalchemy_session.query(Documents).all()
    else:
        documents = db.sqlalchemy_session.query(Documents).join(Users, Users.user_id == Documents.user_id).filter(
            Users.username == username).all()

    documents_upload_date = {}

    for document in documents:
        key = document.document_upload_date
        if key in documents_upload_date:
            documents_upload_date[key] += 1
        else:
            documents_upload_date[key] = 1

    return documents_upload_date
