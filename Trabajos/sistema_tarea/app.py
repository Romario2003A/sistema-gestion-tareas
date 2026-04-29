from flask import Flask, render_template, request, redirect, url_for
from models import Tarea, inicializar_db

app = Flask(__name__)

# 1. Crear la tabla en MySQL automáticamente antes de arrancar
with app.app_context():
    inicializar_db()

# --- RUTAS DEL CRUD ---

# READ: Mostrar todas las tareas
@app.route('/')
def index():
    todas_las_tareas = Tarea.select().order_by(Tarea.id.desc())
    return render_template('index.html', tareas=todas_las_tareas)

# CREATE: Añadir una nueva tarea
@app.route('/crear', methods=['POST'])
def crear():
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    
    # Aquí el ORM Peewee hace la magia del INSERT INTO
    Tarea.create(titulo=titulo, descripcion=descripcion)
    return redirect(url_for('index'))

# UPDATE: Cambiar el estado de la tarea
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    tarea = Tarea.get_by_id(id)
    # Alternar entre Pendiente y Completada
    if tarea.estado == 'Pendiente':
        tarea.estado = 'Completada'
    else:
        tarea.estado = 'Pendiente'
        
    tarea.save() # Peewee hace el UPDATE
    return redirect(url_for('index'))

# DELETE: Borrar una tarea
@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    tarea = Tarea.get_by_id(id)
    tarea.delete_instance() # Peewee hace el DELETE
    return redirect(url_for('index'))

# Arrancar el servidor
if __name__ == '__main__':
    app.run(debug=True)