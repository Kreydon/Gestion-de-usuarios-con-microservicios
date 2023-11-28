import json
from datetime import datetime

import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

update = Flask(__name__)
CORS(update)

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


@update.route("/read_users/<int:id_usuario>", methods=["GET"])
def obtener_usuario_por_id(id_usuario):
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


@update.route("/update_users/<int:user_id>", methods=["POST"])
def update_user(user_id):
    try:
        connection_user = get_user_db_connection()
        cursor_user = connection_user.cursor()

        connection_log = get_log_db_connection()
        cursor_log = connection_log.cursor()

        data = request.get_json()

        cursor_user.execute(
            "SELECT * FROM usuarios WHERE noDocumento = %s AND estado = 'A'",
            (data["noDocumento"],),
        )
        existing_user = cursor_user.fetchone()

        if not existing_user:
            return jsonify({"error": "No existe el usuario"}), 400

        cursor_user.execute(
            """UPDATE usuarios
                SET estado = 'P'
                WHERE (noDocumento = %s) and (estado = 'A');""",
            (data["noDocumento"],),
        )

        insert_query = "INSERT INTO usuarios (tipoDocumento, noDocumento, firstName, secondName, apellidos, fechaNacimiento, genero, correoElectronico, celular, fechaActualizacion, estado, foto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'A', %s)"

        fecha_hora_actual = datetime.now()
        fecha_formateada = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")

        cursor_user.execute(
            insert_query,
            (
                data["tipoDocumento"],
                data["noDocumento"],
                data["firstName"],
                data.get("secondName", None),
                data["apellidos"],
                data["fechaNacimiento"],
                data["genero"],
                data["correoElectronico"],
                data["celular"],
                fecha_formateada,
                json.dumps(data.get("foto", None)),
            ),
        )

        usuario = (data["firstName"]) + " " + (data["apellidos"])
        accion = "Se actualizo el usuario"

        query = "INSERT INTO logz (noDocumento, usuario, accion, fechaAccion, tipoDocumento) VALUES (%s, %s, %s, %s, %s)"
        cursor_log.execute(
            query,
            (
                data["noDocumento"],
                usuario,
                accion,
                fecha_formateada,
                data["tipoDocumento"],
            ),
        )

        connection_user.commit()
        connection_log.commit()
        return jsonify({"mensaje": "Usuario actualizado correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor_user.close()
        connection_user.close()
        cursor_log.close()
        connection_log.close()


if __name__ == "__main__":
    update.run(debug=True, port=5002, host="0.0.0.0")
