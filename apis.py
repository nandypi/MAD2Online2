from flask_restful import Api, Resource
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from models import Item, db, User

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
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            return {'message': 'Email and password are required!'}, 400
        user = User.query.filter_by(email=data['email']).first()
        if not user or user.password != data['password']:
            return {'message': 'Invalid email or password!'}, 401
        access_token = create_access_token(identity=user.email)
        return {'message': 'Login Successful!', 'access_token': access_token}
api.add_resource(Login, '/login')

def is_admin(email):
    user = User.query.filter_by(email=email).first()
    return user and user.role == 'admin'

class Items(Resource):
    @jwt_required()
    def get(self, item_id=None):
        if item_id is not None:
            item = Item.query.get(item_id)
            if not item:
                return {'message': 'Item not found!'}, 404
            return {"message": "Item retrieved successfully!", "item": {'id': item.id, 'name': item.name, 'description': item.description, 'image_url': item.image_url}}
        items = Item.query.all()
        return {"message": "Items retrieved successfully!", "items": [{'id': item.id, 'name': item.name, 'description': item.description, 'image_url': item.image_url} for item in items]}
    @jwt_required()
    def post(self):
        if not is_admin(get_jwt_identity()):
            return {'message': 'Admin privileges required!'}, 403
        
        data = request.get_json()
        if not data or 'name' not in data:
            return {'message': 'Name is required!'}, 400
        new_item = Item(name=data['name'], description=data.get('description'), image_url=data.get('image_url'))
        db.session.add(new_item)
        db.session.commit()
        return {'message': 'Item created successfully!'}
    @jwt_required()
    def put(self, item_id):
        if not is_admin(get_jwt_identity()):
            return {'message': 'Admin privileges required!'}, 403
        
        item = Item.query.get(item_id)
        if not item:
            return {'message': 'Item not found!'}, 404
        data = request.get_json()
        if not data or 'name' not in data:
            return {'message': 'Name is required!'}, 400
        item.name = data['name']
        item.description = data.get('description')
        item.image_url = data.get('image_url')
        db.session.commit()
        return {'message': 'Item updated successfully!'}
    @jwt_required()
    def delete(self, item_id):
        if not is_admin(get_jwt_identity()):
            return {'message': 'Admin privileges required!'}, 403
        
        item = Item.query.get(item_id)
        if not item:
            return {'message': 'Item not found!'}, 404
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Item deleted successfully!'}
api.add_resource(Items, '/items', '/items/<int:item_id>')