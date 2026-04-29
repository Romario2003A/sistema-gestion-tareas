from flask import Flask, render_template, request, redirect, url_for
from models import Tarea, inicializar_db

app = Flask(__name__)

with app.app_context():
    inicializar_db()

# --- RUTAS DEL SISTEMA ---

@app.route('/')
def index():
    # Capturar parámetros de búsqueda y filtro
    busqueda = request.args.get('buscar', '')
    filtro_estado = request.args.get('estado', 'Todos')

    # Consulta base
    query = Tarea.select()

    # Aplicar búsqueda dinámica (Módulo de Búsqueda)
    if busqueda:
        query = query.where(Tarea.titulo.contains(busqueda) | Tarea.descripcion.contains(busqueda))

    # Aplicar filtro de estado (Módulo de Filtros)
    if filtro_estado != 'Todos':
        query = query.where(Tarea.estado == filtro_estado)

    todas_las_tareas = query.order_by(Tarea.id.desc())
    
    return render_template('index.html', tareas=todas_las_tareas, busqueda=busqueda, filtro_estado=filtro_estado)

@app.route('/crear', methods=['POST'])
def crear():
    # Recibir todos los datos del nuevo formulario
    Tarea.create(
        titulo=request.form['titulo'],
        descripcion=request.form['descripcion'],
        prioridad=request.form.get('prioridad', 'Media'),
        fecha_limite=request.form.get('fecha_limite') or None
    )
    return redirect(url_for('index'))

@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    tarea = Tarea.get_by_id(id)
    if tarea.estado == 'Pendiente':
        tarea.estado = 'Completada'
    else:
        tarea.estado = 'Pendiente'
    tarea.save()
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    tarea = Tarea.get_by_id(id)
    tarea.delete_instance()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)