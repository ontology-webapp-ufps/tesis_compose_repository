import hashlib
import json
import hashlib
from unittest import TestCase

from models.models import UserSchema, db, User, Rol
from app import app

users_schema = UserSchema()

class TestUserView(TestCase):
    
    def setUp(self):
        self.created_users = []       
        self.client = app.test_client()

        self.user_one = User(
            name = 'Fulanito de tal',
            email = 'test_ontology_webapp123456789@ufps.edu.co',
            contrasena = '123456',
            rol = Rol.CONSULTOR
        )
        self.created_users.append(self.user_one)

        self.user_two = User(
            name = "Pepito Perez",
            email = 'test123456789@ontology_webapp.com',
            contrasena = '123456',
            rol = Rol.CONSULTOR
        )
        self.created_users.append(self.user_two)

    def tearDown(self):
        for user in self.created_users:
            db_data = User.query.filter(User.email == user.email).first()
            if db_data is not None:
                db.session.delete(db_data)
        db.session.commit()
    
    def test_post_register_users_sucess(self):
        endpoint = "/singin"
        headers = {'Content-Type': 'application/json'}

        response_data = json.loads(self.client.post(endpoint, data=json.dumps(users_schema.dump(self.user_one)), headers=headers).get_data())
        self.assertEqual(int(response_data['api_code']), 1)

        response_data2 = json.loads(self.client.post(endpoint, data=json.dumps(users_schema.dump(self.user_two)), headers=headers).get_data())
        self.assertEqual(int(response_data2['api_code']), 1)
        
    def test_post_register_user_failed_by_repeat(self):
        endpoint = "/singin"
        headers = {'Content-Type': 'application/json'}

        response_data = json.loads(self.client.post(endpoint, data=json.dumps(users_schema.dump(self.user_one)), headers=headers).get_data())
        self.assertEqual(int(response_data['api_code']), 1)

        response_data2 = json.loads(self.client.post(endpoint, data=json.dumps(users_schema.dump(self.user_one)), headers=headers).get_data())
        self.assertEqual(int(response_data2['api_code']), 2)
        
    def test_post_register_user_failed_by_structure(self):
        user_temp = User(
            name = 'Fulanito de tal',
            email = 'test@ufps.edu.co',
            rol = Rol.CONSULTOR
        )

        endpoint = "/singin"
        headers = {'Content-Type': 'application/json'}

        response_data = json.loads(self.client.post(endpoint, data=json.dumps(users_schema.dump(user_temp)), headers=headers).get_data())
        self.assertEqual(int(response_data['api_code']), 2)
        
    def test_post_login_user(self):
        contrasena_original = self.user_one.contrasena
        contrasena_encriptada = hashlib.md5(self.user_one.contrasena.encode('utf-8')).hexdigest()
        self.user_one.contrasena = contrasena_encriptada
        db.session.add(self.user_one)
        db.session.commit()

        data = {}
        data['email'] = self.user_one.email
        data['contrasena'] = contrasena_original

        endpoint = "/login"
        headers = {'Content-Type': 'application/json'}

        response_data = json.loads(self.client.post(endpoint, data=json.dumps(data), headers=headers).get_data())
        self.assertEqual(int(response_data['api_code']), 1)
        self.assertEqual(response_data['user']['email'], self.user_one.email)
        self.assertEqual(response_data['user']['rol'], self.user_one.rol)
        self.assertEqual(response_data['user']['name'], self.user_one.name)
        self.assertEqual(response_data['user']['contrasena'], self.user_one.contrasena)

    def test_post_login_user_failed_credentials(self):
        contrasena_encriptada = hashlib.md5(self.user_one.contrasena.encode('utf-8')).hexdigest()
        self.user_one.contrasena = contrasena_encriptada
        db.session.add(self.user_one)
        db.session.commit()

        data = {}
        data['email'] = self.user_one.email
        data['contrasena'] = self.user_one.contrasena

        endpoint = "/login"
        headers = {'Content-Type': 'application/json'}

        response_data = json.loads(self.client.post(endpoint, data=json.dumps(data), headers=headers).get_data())
        self.assertEqual(int(response_data['api_code']), 2)

    def test_post_login_user_failed_structure(self):
        contrasena_encriptada = hashlib.md5(self.user_one.contrasena.encode('utf-8')).hexdigest()
        self.user_one.contrasena = contrasena_encriptada
        db.session.add(self.user_one)
        db.session.commit()

        data = {}
        data['email'] = self.user_one.email

        endpoint = "/login"
        headers = {'Content-Type': 'application/json'}

        response_data = json.loads(self.client.post(endpoint, data=json.dumps(data), headers=headers).get_data())
        self.assertEqual(int(response_data['api_code']), 2)

    def test_post_validate_jpa_api_access(self):
        token = self.authenticated_user_obtain_token()
        endpoint = "/validate"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(token)}

        response_data = json.loads(self.client.post(endpoint, data={}, headers=headers).get_data())
        self.assertEqual(int(response_data['api_code']), 1)

    def test_post_user_report(self):
        token = self.authenticated_user_obtain_token()
        endpoint = "/user_report"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(token)}

        db.session.add(self.user_two)
        db.session.commit()

        response_data = json.loads(self.client.get(endpoint, headers=headers).get_data())
        self.assertGreater(len(response_data), 0)

    def test_post_update_user_failed_dont_exist(self):
        token = self.authenticated_user_obtain_token()
        endpoint = "/update_user"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(token)}

        data = {}
        data['id'] = -1
        data['rol'] = Rol.ADMINISTRADOR
        data['name'] = self.user_two.name
        data['email'] = self.user_two.email
        data['cambio_contrasena'] = False

        response_data = json.loads(self.client.post(endpoint, data=json.dumps(users_schema.dump(self.user_two)), headers=headers).get_data())
        self.assertEqual(int(response_data['api_code']), 2)

    def test_post_update_user_failed_structure(self):
        token = self.authenticated_user_obtain_token()
        endpoint = "/update_user"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(token)}
        response_data = json.loads(self.client.post(endpoint, data={}, headers=headers).get_data())
        self.assertEqual(int(response_data['api_code']), 2)
    
    def test_post_update_user_sucess_without_password_change(self):
        token = self.authenticated_user_obtain_token()
        endpoint = "/update_user"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(token)}

        db.session.add(self.user_two)
        db.session.commit()

        data = {}
        data['id'] = self.user_two.id
        data['rol'] = Rol.ADMINISTRADOR
        data['name'] = self.user_two.name
        data['email'] = self.user_two.email
        data['cambio_contrasena'] = False

        response_data = json.loads(self.client.post(endpoint, data=json.dumps(data), headers=headers).get_data())
        self.assertEqual(int(response_data['api_code']), 1)        
        self.assertEqual(int(response_data['user']['rol']), 1)

        data['rol'] = Rol.CONSULTOR

        response_data = json.loads(self.client.post(endpoint, data=json.dumps(data), headers=headers).get_data())
        self.assertEqual(int(response_data['api_code']), 1)        
        self.assertEqual(int(response_data['user']['rol']), 2)

    def test_post_update_user_sucess_with_password_change(self):
        token = self.authenticated_user_obtain_token()
        endpoint = "/update_user"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(token)}

        db.session.add(self.user_two)
        db.session.commit()

        data = {}
        data['id'] = self.user_two.id
        data['rol'] = Rol.ADMINISTRADOR
        data['name'] = self.user_two.name
        data['email'] = self.user_two.email
        data['cambio_contrasena'] = True
        data['contrasena'] = '123456789'

        response_data = json.loads(self.client.post(endpoint, data=json.dumps(data), headers=headers).get_data())
        self.assertEqual(int(response_data['api_code']), 1)        
        self.assertEqual(response_data['user']['contrasena'], hashlib.md5(data['contrasena'].encode('utf-8')).hexdigest())

    def test_post_delete_user_sucess(self):
        token = self.authenticated_user_obtain_token()
        endpoint = "/delete_user"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(token)}

        db.session.add(self.user_two)
        db.session.commit()

        data = {}
        data['id'] = self.user_two.id

        response_data = json.loads(self.client.post(endpoint, data=json.dumps(data), headers=headers).get_data())        
        self.assertEqual(int(response_data['api_code']), 1)


    def test_post_delete_user_failed_dont_exist(self):
        token = self.authenticated_user_obtain_token()
        endpoint = "/delete_user"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(token)}

        db.session.add(self.user_two)
        db.session.commit()

        data = {}
        data['id'] = -1

        response_data = json.loads(self.client.post(endpoint, data=json.dumps(data), headers=headers).get_data())
        self.assertEqual(int(response_data['api_code']), 2)

    def test_post_delete_user_failed_bad_structure(self):
        token = self.authenticated_user_obtain_token()
        endpoint = "/delete_user"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(token)}

        db.session.add(self.user_two)
        db.session.commit()

        data = {}
        data['code'] = 1

        response_data = json.loads(self.client.post(endpoint, data=json.dumps(data), headers=headers).get_data())
        self.assertEqual(int(response_data['api_code']), 2)

    def authenticated_user_obtain_token(self):
        contrasena_original = self.user_one.contrasena
        contrasena_encriptada = hashlib.md5(self.user_one.contrasena.encode('utf-8')).hexdigest()
        self.user_one.contrasena = contrasena_encriptada
        db.session.add(self.user_one)
        db.session.commit()

        data = {}
        data['email'] = self.user_one.email
        data['contrasena'] = contrasena_original

        endpoint = "/login"
        headers = {'Content-Type': 'application/json'}

        response_data = json.loads(self.client.post(endpoint, data=json.dumps(data), headers=headers).get_data())

        return response_data['token']

