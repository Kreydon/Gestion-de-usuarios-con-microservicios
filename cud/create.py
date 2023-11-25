import mysql.connector
from flask import Flask, jsonify, request

create = Flask(__name__)

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


@app.route("/users", methods=["POST"])
def agregar_usuario():
    try:
        connection = get_user_db_connection()
        cursor = connection.cursor()

        datos = request.get_json()

        cursor.execute(
            "SELECT * FROM usuarios WHERE noDocumento = %s AND estado = 'A'",
            (datos["noDocumento"],),
        )
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({"error": "Ya existe un usuario con el mismo ID"}), 400

        consulta = "INSERT INTO usuarios (tipoDocumento, noDocumento, firstName, secondName, apellidos, fechaNacimiento, genero, correoElectronico, celular, fechaActualizacion, estado, foto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'A', %s)"

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
                datos["fechaActualizacion"],
                datos.get("foto", None),
            ),
        )

        connection.commit()
        return jsonify({"mensaje": "Usuario agregado correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        connection.close()


@app.route("/logs", methods=["POST"])
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
    create.run(debug=True)
