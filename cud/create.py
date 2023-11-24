import pymysql


class DATABASE:
    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost", user="root", password="14062003", db="gestion_usuarios"
        )

        self.cursor = self.connection.cursor()

        print("😃")

    def crear_usuarios(self, user_data):
        query = """INSERT INTO usuarios 
                    (tipoDocumento, noDocumento, firstName, secondName, apellidos, fechaNacimiento, genero, correoElectronico, celular, fechaActualizacion, estado, foto)
                    VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

        values = (
            user_data["tipoDocumento"],
            user_data["noDocumento"],
            user_data["firstName"],
            user_data.get("secondName", None),
            user_data["apellidos"],
            user_data["fechaNacimiento"],
            user_data["genero"],
            user_data["correoElectronico"],
            user_data["celular"],
            user_data["fechaActualizacion"],
            user_data["estado"],
            user_data.get("foto", None)
        )

        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Usuario creado exitosamente")
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            self.connection.rollback()
            raise
        finally:
            self.close()

    def close(self):
        self.connection.close()


database = DATABASE()

database.crear_usuarios()

database.close()
