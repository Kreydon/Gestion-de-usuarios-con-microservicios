import pymysql


class DATABASE:
    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost", user="root", password="14062003", db="gestion_usuarios"
        )

        self.cursor = self.connection.cursor()

        print("😃")

    def actualizar_usuarios(self):
        update_query = """UPDATE usuarios
                        SET estado = 'P'
                        WHERE (noDocumento = 12345) and (estado = 'A');"""

        insert_query = """INSERT INTO usuarios 
                        (tipoDocumento, noDocumento, firstName, apellidos, fechaNacimiento, genero, correoElectronico, celular, fechaActualizacion, estado)
                        VALUES
                        ('Cédula', 12345, 'Juan', 'Sanchez', '1990-05-29', 'Masculino', 'juanperez@email.com', '3001234567', '2004-02-14', 'A');"""

        try:
            self.cursor.execute(update_query)
            self.connection.commit()

            self.cursor.execute(insert_query)
            self.connection.commit()

        except Exception as e:
            print(f"Error: {e}")
            self.connection.rollback()
            raise

    def close(self):
        self.connection.close()


database = DATABASE()

database.actualizar_usuarios()

database.close()
