import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)

# MySQL database configuration for user management
user_db_config = {
    "host": "localhost",
    "user": "root",
    "password": "14062003",
    "database": "gestion_usuarios",
}

# MySQL database configuration for logs
log_db_config = {
    "host": "localhost",
    "user": "root",
    "password": "14062003",
    "database": "gestion_usuarios",  # Update with your actual log database name
}

# Function to get a database connection for user management
def get_user_db_connection():
    return mysql.connector.connect(**user_db_config)


# Function to get a database connection for logs
def get_log_db_connection():
    return mysql.connector.connect(**log_db_config)


# Endpoint to get a user by ID
@app.route("/usuarios/<int:id_usuario>", methods=["GET"])
def obtener_usuario_por_id(id_usuario):
    try:
        connection = get_user_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = """SELECT tipoDocumento, noDocumento, firstName, apellidos, fechaNacimiento
                   FROM usuarios
                   WHERE noDocumento=%s AND estado = 'A';"""
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


# Endpoint to add a new user
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


# Endpoint to update a user
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


# Endpoint to delete a user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        connection = get_user_db_connection()
        cursor = connection.cursor()

        data = request.get_json()

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


# Endpoint to get all logs
@app.route("/logs", methods=["GET"])
def get_logs():
    try:
        connection = get_log_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM logz")
        logs = cursor.fetchall()
        return jsonify(logs)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        connection.close()


# Endpoint to add a new log entry
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
    app.run(debug=True)
