from dao.db import PostgresDb


def execute_sql(path):
    with open(path) as fp:
        db = PostgresDb()
        engine = db.sqlalchemy_engine
        text = fp.read()
        engine.execute(text)
