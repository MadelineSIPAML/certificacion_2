from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.pelicula import Pelicula
from flask_app.models.comentario import Comentario

@app.route('/peliculas')
@app.route('/dashboard')  # Agregando la ruta dashboard
def peliculas():
    if 'usuario_id' not in session:
        return redirect('/')
    
    peliculas = Pelicula.obtener_todas()
    return render_template('dashboard.html', peliculas=peliculas)

@app.route('/nueva/pelicula')
def nueva_pelicula():
    if 'usuario_id' not in session:
        return redirect('/')
    
    return render_template('nueva_pelicula.html')

@app.route('/crear_pelicula', methods=['POST'])
def crear_pelicula():
    if 'usuario_id' not in session:
        return redirect('/')
    
    try:
        # Validar los datos del formulario
        if not Pelicula.validar_pelicula(request.form):
            # BONUS: Mantener los datos del formulario en caso de error
            return render_template('nueva_pelicula.html', form_data=request.form)
        
        # Preparar los datos para insertar
        data = {
            'titulo': request.form.get('titulo', '').strip(),
            'director': request.form.get('director', '').strip(), 
            'genero': request.form.get('genero', '').strip(),
            'anio': request.form.get('anio', ''),
            'sinopsis': request.form.get('sinopsis', '').strip(),
            'usuario_id': session['usuario_id']
        }
        
        # Crear la película
        Pelicula.crear_pelicula(data)
        flash("Película creada exitosamente.", "success")
        
        return redirect('/dashboard')
        
    except Exception as e:
        flash(f"Error al crear la película: {str(e)}", "pelicula")
        return render_template('nueva_pelicula.html', form_data=request.form)

@app.route('/ver_pelicula/<int:id>')
def ver_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    data = {'id': id}
    pelicula = Pelicula.obtener_por_id(data)
    
    if not pelicula:
        flash("Película no encontrada.", "error")
        return redirect('/dashboard')
    
    # BONUS: Obtener comentarios de la película
    comentarios = Comentario.obtener_por_pelicula(id)
    
    return render_template('ver_pelicula_new.html', pelicula=pelicula, comentarios=comentarios)

@app.route('/editar_pelicula/<int:id>')
def editar_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    data = {'id': id}
    pelicula = Pelicula.obtener_por_id(data)
    
    if not pelicula:
        flash("Película no encontrada.", "error")
        return redirect('/dashboard')
    
    # Verificar que el usuario sea el propietario de la película
    if pelicula['usuario_id'] != session['usuario_id']:
        flash("No tienes permisos para editar esta película.", "error")
        return redirect('/dashboard')
    
    return render_template('editar_pelicula_final.html', pelicula=pelicula)

@app.route('/actualizar_pelicula/<int:id>', methods=['POST'])
def actualizar_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    try:
        # Validar los datos del formulario (pasando el ID para validación única)
        if not Pelicula.validar_pelicula(request.form, id):
            # BONUS: Mantener los datos del formulario en caso de error
            data = {'id': id}
            pelicula = Pelicula.obtener_por_id(data)
            return render_template('editar_pelicula_final.html', pelicula=pelicula, form_data=request.form)
        
        # Preparar los datos para actualizar
        data = {
            'id': id,
            'titulo': request.form.get('titulo', '').strip(),
            'director': request.form.get('director', '').strip(),
            'genero': request.form.get('genero', '').strip(),
            'anio': request.form.get('anio', ''),
            'sinopsis': request.form.get('sinopsis', '').strip(),
            'usuario_id': session['usuario_id']
        }
        
    except Exception as e:
        flash(f"Error al actualizar la película: {str(e)}", "pelicula")
        data = {'id': id}
        pelicula = Pelicula.obtener_por_id(data)
        return render_template('editar_pelicula_final.html', pelicula=pelicula, form_data=request.form)
    
    # Actualizar la película
    Pelicula.actualizar_pelicula(data)
    flash("Película actualizada exitosamente.", "success")
    
    return redirect('/dashboard')

@app.route('/eliminar_pelicula/<int:id>')
def eliminar_pelicula(id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    data = {
        'id': id,
        'usuario_id': session['usuario_id']
    }
    
    # Eliminar la película
    Pelicula.eliminar_pelicula(data)
    flash("Película eliminada exitosamente.", "success")
    
    return redirect('/dashboard')