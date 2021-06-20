import json

from flask import Flask, request
from flask_cors import CORS
from database_worker import DBWorker
import hashlib
from flask_login import LoginManager, login_required, login_user, logout_user

app = Flask(__name__)
app.secret_key = b'_5#yfsdf43g2L"F4Q8rege3]/'

cors = CORS(app, resources={r"/*": {"origins": "*"}})

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/', methods=['GET', 'POST'])
@login_required
def test():
    return 'pr'


@app.route("/api/project/create", methods=['GET', 'POST'])
def createProject():
    token = request.headers.environ['HTTP_AUTHORIZATION']
    data = request.get_json()
    create = DBWorker()
    user = create.getUser(password=token)
    create.createProject(userID=user.id, project_name=data['name'], region=data['region'])
    return 'ok'


@app.route("/api/project/delete", methods=['GET', 'POST'])
def deleteProject():
    token = request.headers.environ['HTTP_AUTHORIZATION']
    data = request.get_json()
    delete = DBWorker()
    try:
        project = delete.getProject(data['id'], token)
        delete.deleteProject(id=project.id)
    except:
        return 'Not Allowed'
    return 'ok'


@app.route("/api/project/update", methods=['GET', 'POST'])
def updateProject():
    # принять параметры и отправить на создание
    update = DBWorker()
    project = update.getProjectById(id=7)
    project.project_name = 'lulzy'
    update.updateProject(project)
    return 'ok'


@app.route("/api/projects/get", methods=['GET', 'POST'])
@login_required
def getProjects():
    token = request.headers.environ['HTTP_AUTHORIZATION']
    datapp = []
    data = request.get_json()
    update = DBWorker()
    project = update.getUserProjects(token)
    for item in project:
        datapp.append({'title': item.project_name, 'id': item.id})
    return json.dumps(datapp)

@app.route("/api/project/get", methods=['GET', 'POST'])
@login_required
def getProject():
    token = request.headers.environ['HTTP_AUTHORIZATION']
    datapp = []
    data = request.get_json()
    update = DBWorker()
    try:
        project = update.getProject(data['id'], token)
        datapp.append({'title': project.project_name, 'id': project.id})
        return json.dumps(datapp)
    except:
        return 'Not Allowed'


@app.route("/api/user/create", methods=['GET', 'POST'])
def createUser():
    data = request.get_json()
    create = DBWorker()
    hashed = hashlib.md5(data['password'].encode())
    create.createUser(username=data['username'], password=hashed.hexdigest())
    return 'ok'


@app.route("/api/user/delete", methods=['GET', 'POST'])
def deleteUser():
    # принять параметры и отправить на создание
    delete = DBWorker()
    delete.deleteUser(id=7)
    return 'ok'


@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    data['password'] = hashlib.md5(data['password'].encode()).hexdigest()
    login = DBWorker()
    user = login.getUser(**data)
    if not user:
        return 'False'
    return user.password


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    token = request.headers.environ['HTTP_AUTHORIZATION']
    logout = DBWorker()
    user = logout.getUser(password=token)
    if user:
        logout_user()
    return 'logged out'


@login_manager.request_loader
def loginGetter(request):
    token = request.headers.environ['HTTP_AUTHORIZATION']
    login = DBWorker()
    try:
        user = login.getUser(password=token)
    except:
        return 'Not Logged'
    return user
