from flask import Flask, request, render_template


app = Flask(__name__)

# connecting to the apis
from apis import api
api.init_app(app)

# connecting to the database
from models import db, User
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.route('/mad1')
def mad1_api():
    return render_template('index.html', message='Hello from MAD1!')

@app.route('/mad2', methods=['GET', 'POST'])
def mad2_api():
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'name' not in data:
            return {'message': 'Name is required!'}, 400
        return {'message': f'Hello, {data["name"]}!'}
    return {'message': 'Hello from MAD2!'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        is_admin = User.query.filter_by(role='admin').first()
        if not is_admin:
            admin_user = User(name='Admin', role='admin', email='admin@example.com', password='password')
            db.session.add(admin_user)
            db.session.commit()
            is_admin = admin_user
            print('Admin user created.')
        print('Admin user credentials:')
        print(f'Name: {is_admin.email}')
        print(f'Password: {is_admin.password}')
    app.run(debug=True)