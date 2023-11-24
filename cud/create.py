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

    def crear_usuarios(self, usuario):
        query = f"""INSERT INTO usuarios 
                    (tipoDocumento, noDocumento, firstName, apellidos, fechaNacimiento, genero, correoElectronico, celular, fechaActualizacion, estado)
                    VALUES
                    ('{usuario['tipoDocumento']}', {usuario['noDocumento']}, '{usuario['firstName']}', '{usuario['apellidos']}', '{usuario['fechaNacimiento']}', '{usuario['genero']}', '{usuario['correoElectronico']}', '{usuario['celular']}', '{usuario['fechaActualizacion']}', '{usuario['estado']}');"""
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
    database.crear_usuarios(usuario)
database.close()
