from flask_restful import Api, Resource
from flask import request

from models import db, User

api = Api()

class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, World!'}
    def post(self):
        data = request.get_json()
        if not data or 'name' not in data:
            return {'message': 'Name is required!'}, 400
        return {'message': f'Hello, {data["name"]}!'}
api.add_resource(HelloWorld, '/api')

class Register(Resource):
    def post(self):
        data = request.get_json()
        if not data or 'name' not in data or 'email' not in data or 'password' not in data:
            return {'message': 'Name, email, and password are required!'}, 400
        if not all([data['name'], data['email'], data['password']]):
            return {'message': 'Name, email, and password cannot be empty!'}, 400
        is_existing_user = User.query.filter_by(email=data['email']).first()
        if is_existing_user:
            return {'message': 'User with this email already exists!'}, 400
        new_user = User(name=data['name'], email=data['email'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User registered successfully!'}
api.add_resource(Register, '/register')

class Login(Resource):
    def post(self):
        return {'message': 'Login Successful!'}
api.add_resource(Login, '/login')

class AllUsers(Resource):
    def get(self):
        users = User.query.all()
        users = [{'name': user.name, 'email': user.email, 'role': user.role} for user in users]
        return {'message':'All users retrieved successfully!', 'users': users}
api.add_resource(AllUsers, '/users')