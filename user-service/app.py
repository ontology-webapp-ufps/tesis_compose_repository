from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from models.models import db

from views.user_views import ViewAuth, ViewDelete, ViewLogin, ViewReport, ViewSingIn, ViewUpdate

app = Flask(__name__)
db_host = 'users_database'
db_port = 5432
db_name = 'USER_DB'
db_password = 'USER_PASSWORD_ULTA_SECRETO'
db_user = 'USER_USER_DB'

connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)

api.add_resource(ViewSingIn, '/singin')
api.add_resource(ViewLogin, '/login')
api.add_resource(ViewAuth, '/validate')

api.add_resource(ViewReport, '/user_report')
api.add_resource(ViewUpdate, '/update_user')
api.add_resource(ViewDelete, '/delete_user')

jwt = JWTManager(app)