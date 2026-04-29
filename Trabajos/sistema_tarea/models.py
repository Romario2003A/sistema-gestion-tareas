from peewee import *

# 1. Configuramos la conexión a la base de datos
db = MySQLDatabase(
    'gestion_tareas',   
    user='root',        
    password='root',        # <- Revisa tu contraseña aquí
    host='localhost',
    port=3306
)

# 2. Definimos el Modelo (La tabla)
class Tarea(Model):
    titulo = CharField(max_length=150)
    descripcion = TextField()
    estado = CharField(default='Pendiente')

    class Meta:
        database = db
        table_name = 'tareas'

# 3. Función para inicializar
def inicializar_db():
    db.connect()
    db.create_tables([Tarea], safe=True)
    db.close()