import pymysql


class DATABASE:
    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost", user="root", password="14062003", db="gestion_usuarios"
        )

        self.cursor = self.connection.cursor()

        print("😃")

    def eliminar_usuarios(self):
        query = f"""UPDATE usuarios
                    SET estado = 'P'
                    WHERE (noDocumento = 12345) and (estado = 'A');"""
        try:
            self.cursor.execute(query)
            self.connection.commit()

        except Exception as e:
            raise

    def close(self):
        self.connection.close()


database = DATABASE()

database.eliminar_usuarios()

database.close()
