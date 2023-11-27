import requests

""" from delete import DeleteUserResource """
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource

app = Flask(__name__)
CORS(app)
api = Api(app)


class CreateUser(Resource):
    def post(self):
        data = request.get_json()
        resp = requests.post("http://localhost:5001/create_users", json=data)
        return resp.json(), 201  # devolver respuesta


api.add_resource(CreateUser, "/create_users")

""" api.add_resource(ReadUserResource, "/read_users/<int:id_usuario>")
api.add_resource(UpdateUserResource, "/update_users/<int:user_id>")
api.add_resource(DeleteUserResource, "/delete_users/<int:user_id>") """

if __name__ == "__main__":
    app.run(debug=True, port=5000)
