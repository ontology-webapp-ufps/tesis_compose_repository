from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from enum import IntEnum

db = SQLAlchemy()

class Rol(IntEnum):
    ADMINISTRADOR = 1
    CONSULTOR = 2

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(300), unique=True)
    name = db.Column(db.String(300))
    contrasena = db.Column(db.String(32))
    rol = db.Column(db.Enum(Rol))

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True        
        include_fk = True
