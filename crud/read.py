import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource

read = Flask(__name__)
CORS(read)
api = Api(read)

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


class ReadUserResource(Resource):
    def get(self, id_usuario):
        try:
            connection = get_user_db_connection()
            cursor = connection.cursor(dictionary=True)
            query = """SELECT tipoDocumento, noDocumento, firstName, secondName, apellidos, fechaNacimiento, genero, correoElectronico, celular, foto
                    FROM usuarios
                    WHERE (noDocumento=%s) AND (estado = 'A');"""
            cursor.execute(query, (id_usuario,))
            usuario = cursor.fetchone()

            if usuario:
                return jsonify(usuario)
            else:
                return jsonify({"mensaje": "Usuario no encontrado"}), 404
        except Exception as e:
            return jsonify({"error": str(e)})
        finally:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    read.run(debug=True)
