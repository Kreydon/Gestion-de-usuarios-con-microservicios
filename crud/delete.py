from datetime import datetime

import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

delete = Flask(__name__)
CORS(delete)

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


@delete.route("/delete_users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        connection_user = get_user_db_connection()
        cursor_user = connection_user.cursor()

        data = request.get_json()

        cursor_user.execute(
            "SELECT * FROM usuarios WHERE noDocumento = %s AND estado = 'A'",
            (data["noDocumento"],),
        )
        existing_user = cursor_user.fetchone()
        print()

        if not existing_user:
            return jsonify({"error": "No existe el usuario"}), 400

        cursor_user.execute(
            "UPDATE usuarios SET estado = 'P' WHERE noDocumento = %s AND estado = 'A'",
            (data["noDocumento"],),
        )

        connection_user.commit()
        return jsonify({"mensaje": "Usuario eliminado correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor_user.close()
        connection_user.close()


@delete.route("/logs/<int:user_id>", methods=["POST"])
def add_log(user_id):
    try:
        connection_log = get_log_db_connection()
        cursor_log = connection_log.cursor()

        connection_user = get_user_db_connection()
        cursor_user = connection_user.cursor()

        datos = request.get_json()

        cursor_user.execute(
            "SELECT firstName, apellidos, noDocumento, tipoDocumento FROM usuarios WHERE noDocumento = %s AND estado = 'A'",
            (datos["noDocumento"],),
        )
        print(datos["noDocumento"])

        user = cursor_user.fetchone()

        print(user)

        fecha_hora_actual = datetime.now()
        fecha_formateada = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")

        usuario = (user[0]) + " " + (user[1])
        accion = "Se elimino el usuario"

        query = "INSERT INTO logz (noDocumento, usuario, accion, fechaAccion, tipoDocumento) VALUES (%s, %s, %s, %s, %s)"
        cursor_log.execute(
            query,
            (
                user[2],
                usuario,
                accion,
                fecha_formateada,
                user[3],
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
    delete.run(debug=True, port=5003, host="0.0.0.0")
