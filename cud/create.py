import pymysql


class DATABASE:
    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost", user="root", password="14062003", db="gestion_usuarios"
        )

        self.cursor = self.connection.cursor()

        print("😃")

    def crear_usuarios(self):
        query = f"""INSERT INTO usuarios 
                    (tipoDocumento, noDocumento, firstName, apellidos, fechaNacimiento, genero, correoElectronico, celular, fechaActualizacion, estado)
                    VALUES
                    ('Cédula', 12345, 'Juan', 'Perez', '1990-05-29', 'Masculino', 'juanperez@email.com', '3001234567', '2004-02-14', 'A');"""
        try:
            self.cursor.execute(query)
            self.connection.commit()

        except Exception as e:
            raise

    def close(self):
        self.connection.close()


database = DATABASE()

database.crear_usuarios()

database.close()
