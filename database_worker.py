from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Project, Keywords, Users
from database_setup import engine
import sys, os, hashlib


class DBWorker(object):

    def __init__(self):
        # Подключаемся и создаем сессию базы данных
        engine = create_engine('sqlite:///seprparser.db?check_same_thread=False')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def createProject(self, userID, **kwargs):
        newProject = Project(**kwargs)
        user = self.getUser(id=userID)
        user.projects.append(newProject)
        self.session.add(user)
        self.session.commit()
        return 'ok'

    def deleteProject(self, **kwargs):
        deleteProject = self.session.query(Project).filter_by(**kwargs).one()
        self.session.delete(deleteProject)
        self.session.commit()
        return 'ok'

    def getUserProjects(self, token, **kwargs):
        user = self.session.query(Users).filter_by(password=token).one()
        getProject = self.session.query(Project).filter_by(users=user).all()
        return getProject

    def getProject(self, *args, **kwargs):
        id, token = args
        user = self.session.query(Users).filter_by(password=token).one()
        try:
            project = self.session.query(Project).filter_by(id=id).filter_by(users=user).one()
            return project
        except:
            return 'None'

    def updateProject(self, project):
        self.session.add(project)
        self.session.commit()
        return 'ok'

    def createUser(self, **kwargs):
        newUser = Users(**kwargs)
        self.session.add(newUser)
        self.session.commit()
        return 'ok'

    def deleteUser(self, **kwargs):
        deleteUser = self.session.query(Users).filter_by(**kwargs).one()
        self.session.delete(deleteUser)
        self.session.commit()
        return 'ok'

    def getUser(self, **kwargs):
        try:
            getUser = self.session.query(Users).filter_by(**kwargs).one()
        except:
            return False
        return getUser

    def updateUser(self, user):
        self.session.add(user)
        self.session.commit()
        return 'ok'
