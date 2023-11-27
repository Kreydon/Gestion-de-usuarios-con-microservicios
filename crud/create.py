import json
from datetime import datetime

import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource

create = Flask(__name__)
CORS(create)
api = Api(create)

user_db_config = {
    "host": "localhost",
    "user": "root",
    "password": "14062003",
    "database": "gestion_usuarios",
}

""" log_db_config = {
    "host": "localhost",
    "user": "root",
    "password": "14062003",
    "database": "gestion_usuarios",
} """


def get_user_db_connection():
    return mysql.connector.connect(**user_db_config)


""" def get_log_db_connection():
    return mysql.connector.connect(**log_db_config) """


class CreateUserResource(Resource):
    def post(self):
        try:
            connection = get_user_db_connection()
            cursor = connection.cursor()

            datos = request.get_json()

            if not datos:
                return (
                    jsonify({"error": "Datos JSON no proporcionados o no válidos"}),
                    400,
                )

            cursor.execute(
                "SELECT * FROM usuarios WHERE (noDocumento = %s) AND (estado = 'A')",
                (datos["noDocumento"],),
            )
            existing_user = cursor.fetchone()

            if existing_user:
                return jsonify({"error": "Ya existe un usuario con el mismo ID"}), 400

            consulta = "INSERT INTO usuarios (tipoDocumento, noDocumento, firstName, secondName, apellidos, fechaNacimiento, genero, correoElectronico, celular, fechaActualizacion, estado, foto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'A', %s)"

            fecha_hora_actual = datetime.now()
            fecha_formateada = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                consulta,
                (
                    datos["tipoDocumento"],
                    datos["noDocumento"],
                    datos["firstName"],
                    datos.get("secondName", None),
                    datos["apellidos"],
                    datos["fechaNacimiento"],
                    datos["genero"],
                    datos["correoElectronico"],
                    datos["celular"],
                    fecha_formateada,
                    json.dumps(datos.get("foto", None)),
                ),
            )

            connection.commit()
            return jsonify({"mensaje": "Usuario agregado correctamente"})
        except Exception as e:
            return jsonify({"error": str(e)})
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


if __name__ == "__main__":
    create.run(debug=True, host="0.0.0.0")
