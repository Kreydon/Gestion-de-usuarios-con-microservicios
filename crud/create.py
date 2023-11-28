import json
from datetime import datetime

import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

create = Flask(__name__)
CORS(create)

user_db_config = {
    "host": "db",
    "user": "root",
    "database": "gestion_usuarios",
}

""" user_db_config = {
    "host": "localhost",
    "user": "root",
    "password": "14062003",
    "database": "gestion_usuarios",
} """

log_db_config = {
    "host": "db",
    "user": "root",
    "database": "gestion_usuarios",
}


def get_user_db_connection():
    return mysql.connector.connect(**user_db_config)


def get_log_db_connection():
    return mysql.connector.connect(**log_db_config)


@create.route("/create_users", methods=["POST"])
def agregar_usuario():
    try:
        connection_user = get_user_db_connection()
        cursor_user = connection_user.cursor()

        connection_log = get_log_db_connection()
        cursor_log = connection_log.cursor()

        datos = request.get_json()

        if not datos:
            return jsonify({"error": "Datos JSON no proporcionados o no válidos"}), 400

        cursor_user.execute(
            "SELECT * FROM usuarios WHERE (noDocumento = %s) AND (estado = 'A')",
            (datos["noDocumento"],),
        )
        existing_user = cursor_user.fetchone()

        if existing_user:
            return jsonify({"error": "Ya existe un usuario con el mismo ID"}), 400

        consulta = "INSERT INTO usuarios (tipoDocumento, noDocumento, firstName, secondName, apellidos, fechaNacimiento, genero, correoElectronico, celular, fechaActualizacion, estado, foto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'A', %s)"

        fecha_hora_actual = datetime.now()
        fecha_formateada = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")

        cursor_user.execute(
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

        usuario = (datos["firstName"]) + " " + (datos["apellidos"])
        accion = "Se creo el usuario"

        query = "INSERT INTO logz (noDocumento, usuario, accion, fechaAccion, tipoDocumento) VALUES (%s, %s, %s, %s, %s)"
        cursor_log.execute(
            query,
            (
                datos["noDocumento"],
                usuario,
                accion,
                fecha_formateada,
                datos["tipoDocumento"],
            ),
        )

        connection_user.commit()
        connection_log.commit()
        return jsonify({"mensaje": "Usuario agregado correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor_user.close()
        connection_user.close()
        cursor_log.close()
        connection_log.close()


""" @create.route("/logs", methods=["POST"])
def add_log():
    try:
        connection = get_log_db_connection()
        cursor = connection.cursor()

        data = request.get_json()

        query = "INSERT INTO logz (noDocumento, usuario, accion, fechaAccion) VALUES (%s, %s, %s, %s)"
        cursor.execute(
            query,
            (data["noDocumento"], data["usuario"], data["accion"], data["fechaAccion"]),
        )

        connection.commit()
        return jsonify({"mensaje": "Entrada de log agregada correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        connection.close() """


if __name__ == "__main__":
    create.run(debug=True, host="0.0.0.0")
