import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

read = Flask(__name__)
CORS(read)

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


@read.route("/read_users/<int:id_usuario>", methods=["GET"])
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


@read.route("/logs", methods=["POST"])
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
    read.run(debug=True, port=5001)
