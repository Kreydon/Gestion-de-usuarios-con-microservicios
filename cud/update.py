import mysql.connector
from flask import Flask, jsonify, request

update = Flask(__name__)

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


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
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
            """UPDATE usuarios
                SET estado = 'P'
                WHERE (noDocumento = %s) and (estado = 'A');""",
            (data["noDocumento"],),
        )

        insert_query = """INSERT INTO usuarios 
                        (tipoDocumento, noDocumento, firstName, secondName, apellidos, fechaNacimiento, genero, correoElectronico, celular, fechaActualizacion, estado, foto)
                        VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'A', %s);"""

        cursor.execute(
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
                data["fechaActualizacion"],
                data.get("foto", None),
            ),
        )

        connection.commit()
        return jsonify({"mensaje": "Usuario actualizado correctamente"})
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
    update.run(debug=True)
