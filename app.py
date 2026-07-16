from flask import Flask, request, render_template
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

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

class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, World!'}
    def post(self):
        data = request.get_json()
        if not data or 'name' not in data:
            return {'message': 'Name is required!'}, 400
        return {'message': f'Hello, {data["name"]}!'}
api.add_resource(HelloWorld, '/api')

if __name__ == '__main__':
    app.run(debug=True)