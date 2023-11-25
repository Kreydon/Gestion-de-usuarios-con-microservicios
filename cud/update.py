import pymysql
import requests
import json

class DATABASE:
    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost", user="root", password="14062003", db="gestion_usuarios"
        )
        self.cursor = self.connection.cursor()
        print("😃")

    def actualizar_usuarios(self, usuario):
        update_query = f"""UPDATE usuarios
                           SET firstName = '{usuario['firstName']}', apellidos = '{usuario['apellidos']}'
                           WHERE noDocumento = {usuario['noDocumento']};"""

        try:
            self.cursor.execute(update_query)
            self.connection.commit()
        except Exception as e:
            print(f"Error: {e}")
            self.connection.rollback()
            raise

    def close(self):
        self.connection.close()

response = requests.get("URL")
json_data = response.json()

database = DATABASE()
for usuario in json_data['usuarios']:
    database.actualizar_usuarios(usuario)
database.close()
