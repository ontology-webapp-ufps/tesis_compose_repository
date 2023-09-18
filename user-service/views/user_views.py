from flask import request, abort
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
import hashlib

from models.models import db, User, UserSchema, Rol

user_schema = UserSchema()

class ViewSingIn(Resource):
    def post(self):
        try:
            email = request.json['email']

            query_email = User.query.filter(User.email == request.json["email"]).first()

            if query_email is None:
                new_user = User(
                    name = request.json['name'],
                    email = email,
                    contrasena = hashlib.md5(request.json["contrasena"].encode('utf-8')).hexdigest(),
                    rol = Rol.CONSULTOR
                )
                db.session.add(new_user)
                db.session.commit()
                return {"api_code": "1", "mensaje": "Usuario registrado exitosamente."}
            else: 
                return {"api_code": "2", "mensaje": "El correo electronico ya ha sido registrado previamente."}
        except:
            return {"api_code": "2", "mensaje": "El request no tiene la estructura correcta."}
  
class ViewLogin(Resource):
    def post(self):
        try:
            email = request.json['email']
            contrasena = hashlib.md5(request.json["contrasena"].encode('utf-8')).hexdigest()

            login_user = User.query.filter(User.email==email, User.contrasena==contrasena).first()
        
            if login_user is None:
                return {"api_code": "2", "mensaje": "Login fallido, credenciales incorrectas."}
            else:
                token_de_acceso = create_access_token(identity=login_user.id)
                return {"api_code": "1", "mensaje": "Autenticación exitosa", "token": token_de_acceso, "user": user_schema.dump(login_user)}
        except:
            return {"api_code": "2", "mensaje": "El request no tiene la estructura correcta."}

class ViewAuth(Resource):
    @jwt_required()
    def post(self):
        #Si y solo si el JWT es exitoso responderá así
        return {"api_code": "1", "mensaje": "Autenticación exitosa"}

class ViewReport(Resource):
    @jwt_required()
    def get(self):
        users = User.query.all()
        return [user_schema.dump(user) for user in users]
    
class ViewDelete(Resource):
    @jwt_required()
    def post(self):
        try:
            user_query = User.query.get(request.json['id'])

            if user_query is None:
                return {"api_code": "2", "mensaje": "Usuario no existe en el sistema."}
            else:         
                db.session.delete(user_query)        
                db.session.commit()
                return {"api_code": "1", "mensaje": "Usuario eliminado exitosamente."}
        except:
            return {"api_code": "2", "mensaje": "El request no tiene la estructura correcta."}

class ViewUpdate(Resource):
    @jwt_required()
    def post(self):
        try:
            user_query = User.query.get(request.json['id'])

            if user_query is None:
                return {"api_code": "2", "mensaje": "Usuario no existe en el sistema."}
            else: 
                user_query.name = request.json['name']
                user_query.email = request.json['email']

                role = request.json['rol']

                is_change_password = request.json['cambio_contrasena']

                if is_change_password:
                    user_query.contrasena = hashlib.md5(request.json["contrasena"].encode('utf-8')).hexdigest()

                if role == 1:
                    user_query.rol = Rol.ADMINISTRADOR
                else:
                    user_query.rol = Rol.CONSULTOR

                db.session.commit()
                return {"api_code": "1", "mensaje": "Usuario actualizado exitosamente.", "user": user_schema.dump(user_query)}
        except:
            return {"api_code": "2", "mensaje": "El request no tiene la estructura correcta."}

            {
    "postId": "{{OFFER_POSTID}}",
    "description": "{{OFFER_DESCRIPTION}}",
    "size": "{{OFFER_SIZE}}",
    "fragile": {{OFFER_FRAGILE}},
    "offer": {{OFFER_OFFER}}
}