
from sqlalchemy import Column, ForeignKey, Integer, String, Text, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask_login import UserMixin


Base = declarative_base()


class Users(Base, UserMixin):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    projects = relationship("Project", backref="users", lazy='dynamic', cascade="all, delete, delete-orphan")
    username = Column(String(250), nullable=False)
    password = Column(String(50), nullable=False, default='123')


class Project(Base):
    __tablename__ = 'Project'

    id = Column(Integer, primary_key=True)
    project_name = Column(String(250), nullable=False)
    region = Column(String(250), nullable=False)

    user_id = Column(Integer, ForeignKey('Users.id'))
    keywords = relationship("Keywords", backref="project", lazy='dynamic')


class Keywords(Base):
    __tablename__ = 'Keywords'

    id = Column(Integer, primary_key=True)
    keyword_name = Column(String(250), nullable=False)

    project_id = Column(Integer, ForeignKey('Project.id'))





engine = create_engine('sqlite:///seprparser.db')
Base.metadata.create_all(engine)
