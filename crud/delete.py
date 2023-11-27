import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource

delete = Flask(__name__)
CORS(delete)
api = Api(delete)

user_db_config = {
    "host": "localhost",
    "user": "root",
    "password": "14062003",
    "database": "gestion_usuarios",
}

log_db_config = {
    "host": "localhost",
    "user": "root",
    "password": "14062003",
    "database": "gestion_usuarios",
}


def get_user_db_connection():
    return mysql.connector.connect(**user_db_config)


def get_log_db_connection():
    return mysql.connector.connect(**log_db_config)


class DeleteUserResource(Resource):
    def delete(self, user_id):
        try:
            connection = get_user_db_connection()
            cursor = connection.cursor()

            data = request.get_json()

            cursor.execute(
                "SELECT * FROM usuarios WHERE noDocumento = %s AND estado = 'A'",
                (data["noDocumento"],),
            )
            existing_user = cursor.fetchone()

            if not existing_user:
                return jsonify({"error": "No existe el usuario"}), 400

            cursor.execute(
                "UPDATE usuarios SET estado = 'P' WHERE noDocumento = %s AND estado = 'A'",
                (data["noDocumento"],),
            )

            connection.commit()
            return jsonify({"mensaje": "Usuario eliminado correctamente"})
        except Exception as e:
            return jsonify({"error": str(e)})
        finally:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    delete.run(debug=True)
