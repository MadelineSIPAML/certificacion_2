from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.comentario import Comentario

@app.route('/crear_comentario/<int:pelicula_id>', methods=['POST'])
def crear_comentario(pelicula_id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    # BONUS: Verificar que el usuario no sea el creador de la película
    from flask_app.models.pelicula import Pelicula
    data_pelicula = {'id': pelicula_id}
    pelicula = Pelicula.obtener_por_id(data_pelicula)
    
    if not pelicula:
        flash("Película no encontrada.", "error")
        return redirect('/dashboard')
    
    # BONUS: El usuario creador de la película no puede comentar
    if pelicula['usuario_id'] == session['usuario_id']:
        flash("No puedes comentar tu propia película.", "comentario")
        return redirect(f'/ver_pelicula/{pelicula_id}')
    
    # Validar los datos del formulario
    if not Comentario.validar_comentario(request.form):
        return redirect(f'/ver_pelicula/{pelicula_id}')
    
    # Preparar los datos para insertar
    data = {
        'comentario': request.form['comentario'],
        'usuario_id': session['usuario_id'],
        'pelicula_id': pelicula_id
    }
    
    # Crear el comentario
    Comentario.crear_comentario(data)
    flash("Comentario agregado exitosamente.", "success")
    
    return redirect(f'/ver_pelicula/{pelicula_id}')

@app.route('/eliminar_comentario/<int:comentario_id>/<int:pelicula_id>')
def eliminar_comentario(comentario_id, pelicula_id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    data = {
        'id': comentario_id,
        'usuario_id': session['usuario_id']
    }
    
    # Eliminar el comentario (solo si pertenece al usuario en sesión)
    Comentario.eliminar_comentario(data)
    flash("Comentario eliminado exitosamente.", "success")
    
    return redirect(f'/ver_pelicula/{pelicula_id}')