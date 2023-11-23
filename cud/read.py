import pymysql

class DATABASE:
    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost", user="root", password="14062003", db="gestion_usuarios"
        )
        self.cursor = self.connection.cursor()

    def obtener_usuarios(self):
        query = "SELECT * FROM usuarios;"
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except pymysql.Error as e:
            print(f"Error: {e}")
            raise
        finally:
            self.connection.close()
