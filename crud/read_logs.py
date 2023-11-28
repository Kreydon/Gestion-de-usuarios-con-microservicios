import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

read = Flask(__name__)
CORS(read)

log_db_config = {
    "host": "db",
    "user": "root",
    "database": "gestion_usuarios",
}

""" log_db_config = {
    "host": "localhost",
    "user": "root",
    "password": "14062003",
    "database": "gestion_usuarios",
} """


def get_log_db_connection():
    return mysql.connector.connect(**log_db_config)


@read.route("/logs_tipo/<int:id_usuario>/<string:tipoDoc>", methods=["GET"])
def obtener_usuario_por_id(id_usuario, tipoDoc):
    try:
        connection_log = get_log_db_connection()
        cursor_log = connection_log.cursor(dictionary=True)
        query = f"""SELECT tipoDocumento, noDocumento, usuario, accion, fechaAccion 
                   FROM logz
                   WHERE (noDocumento={id_usuario}) AND (tipoDocumento="{tipoDoc}");"""
        cursor_log.execute(query)
        usuario = cursor_log.fetchall()

        if usuario:
            return jsonify(usuario)
        else:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor_log.close()
        connection_log.close()


@read.route("/logs_fecha/<string:fecha>", methods=["GET"])
def obtener_usuario_por_fecha(fecha):
    try:
        connection_log = get_log_db_connection()
        cursor_log = connection_log.cursor(dictionary=True)
        query = f"""SELECT tipoDocumento, noDocumento, usuario, accion, fechaAccion 
                   FROM logz
                   WHERE fechaAccion="{fecha}";"""
        cursor_log.execute(query)
        usuario = cursor_log.fetchall()

        if usuario:
            return jsonify(usuario)
        else:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor_log.close()
        connection_log.close()


if __name__ == "__main__":
    read.run(debug=True, port=5004, host="0.0.0.0")
