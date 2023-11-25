import mysql.connector
from flask import Flask, jsonify, request

delete = Flask(__name__)

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


@delete.route("/delete_users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
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


@delete.route("/logs", methods=["POST"])
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
        connection.close()


if __name__ == "__main__":
    delete.run(debug=True)
