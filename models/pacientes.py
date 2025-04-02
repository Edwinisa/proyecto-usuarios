from conexion import *

class paientes:
    def consulta(self):
        sql = "SELECT * FROM pacientes WHERE borrado=0"
        mi_cursor.cursor.execute(sql)
        pacientes = mi_cursor.fetchall()
        return pacientes