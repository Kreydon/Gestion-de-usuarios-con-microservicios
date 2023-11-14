import pymysql


class DATABASE:
    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost", user="root", password="14062003", db="gestion_usuarios"
        )

        self.cursor = self.connection.cursor()

        print("😃")

    def ver_usuarios(self):
        query = f"""SELECT tipoDocumento, noDocumento, firstName, apellidos, fechaNacimiento
                    FROM usuarios
                    WHERE estado = 'A';"""
        try:
            self.cursor.execute(query)
            infos = self.cursor.fetchall()

            for info in infos:
                print(
                    f"Tipo de documento: {info[0]}\nNo de documento: {info[1]}\nNombre: {info[2]}\nApellidos: {info[3]}\nFecha de nacimiento: {info[4]}"
                )
        except Exception as e:
            raise

    def close(self):
        self.connection.close()


database = DATABASE()

database.ver_usuarios()

database.close()
