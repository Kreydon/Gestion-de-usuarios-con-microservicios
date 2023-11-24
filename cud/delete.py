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

    def eliminar_usuarios(self, noDocumento):
        query = f"""UPDATE usuarios
                    SET estado = 'P'
                    WHERE noDocumento = {noDocumento};"""
        try:
            self.cursor.execute(query)
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
    database.eliminar_usuarios(usuario['noDocumento'])
database.close()
