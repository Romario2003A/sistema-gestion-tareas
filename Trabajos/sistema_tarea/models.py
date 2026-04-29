from peewee import *
from datetime import datetime

# 1. Configuración de la base de datos
db = MySQLDatabase(
    'gestion_tareas',   
    user='root',        
    password='root',        # <-- PON TU CONTRASEÑA AQUÍ
    host='localhost',
    port=3306
)

# 2. Modelo Avanzado (Nuevas columnas de Prioridad y Fecha)
class Tarea(Model):
    titulo = CharField(max_length=150)
    descripcion = TextField()
    estado = CharField(default='Pendiente')
    prioridad = CharField(default='Media')
    fecha_limite = DateField(null=True)

    class Meta:
        database = db
        table_name = 'tareas'

# 3. Inicialización
def inicializar_db():
    db.connect()
    db.create_tables([Tarea], safe=True)
    db.close()