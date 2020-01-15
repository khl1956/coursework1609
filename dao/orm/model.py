from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    password_hash = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)


class Documents(Base):
    __tablename__ = "documents"
    document_id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=False)
    document_name = Column(String, nullable=False)
    document_file_path = Column(String, nullable=False)
    document_upload_date = Column(Date, nullable=False)


class Templates(Base):
    __tablename__ = 'templates'
    template_id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=False)
    template_name = Column(String, nullable=False)
    template_file_path = Column(String, nullable=False)
    template_upload_date = Column(Date, nullable=False)


class Fields(Base):
    __tablename__ = 'fields'

    field_id = Column(Integer, autoincrement=True, primary_key=True)
    template_id = Column(Integer, ForeignKey('templates.template_id'), primary_key=True)
    field_name = Column(String, nullable=False)
    field_content = Column(String, nullable=False)


class UserSessions(Base):
    __tablename__ = 'usersessions'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    session_id = Column(String, primary_key=True)
