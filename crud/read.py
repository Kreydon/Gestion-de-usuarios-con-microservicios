from datetime import datetime

import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

read = Flask(__name__)
CORS(read)

user_db_config = {
    "host": "db",
    "user": "root",
    "database": "gestion_usuarios",
}

log_db_config = {
    "host": "db",
    "user": "root",
    "database": "gestion_usuarios",
}


def get_user_db_connection():
    return mysql.connector.connect(**user_db_config)


def get_log_db_connection():
    return mysql.connector.connect(**log_db_config)


@read.route("/read_users/<int:id_usuario>", methods=["GET"])
def obtener_usuario_por_id(id_usuario):
    try:
        connection_user = get_user_db_connection()
        cursor_user = connection_user.cursor(dictionary=True)
        query = """SELECT tipoDocumento, noDocumento, firstName, secondName, apellidos, fechaNacimiento, genero, correoElectronico, celular, foto
                   FROM usuarios
                   WHERE (noDocumento=%s) AND (estado = 'A');"""
        cursor_user.execute(query, (id_usuario,))
        usuario = cursor_user.fetchone()

        if usuario:
            return jsonify(usuario)
        else:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor_user.close()
        connection_user.close()


@read.route("/logs", methods=["POST"])
def add_log():
    try:
        connection_log = get_log_db_connection()
        cursor_log = connection_log.cursor()

        datos = request.get_json()

        fecha_hora_actual = datetime.now()
        fecha_formateada = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")

        usuario = (datos["firstName"]) + " " + (datos["apellidos"])
        accion = "Se consulto el usuario"

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

        connection_log.commit()
        return jsonify({"mensaje": "Entrada de log agregada correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor_log.close()
        connection_log.close()


if __name__ == "__main__":
    read.run(debug=True, port=5001, host="0.0.0.0")
