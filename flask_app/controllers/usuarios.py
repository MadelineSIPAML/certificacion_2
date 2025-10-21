from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_app import bcrypt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
@app.route('/register', methods=['POST'])  # Ruta adicional para compatibilidad
def registro():
    try:
        # Validar los datos del formulario
        if not Usuario.validar_registro(request.form):
            return redirect('/')
        
        # Encriptar la contraseña
        password_encriptada = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        
        # Preparar los datos para insertar con .get() para evitar KeyError
        data = {
            'nombre': request.form.get('nombre', '').strip(),
            'apellido': request.form.get('apellido', '').strip(),
            'email': request.form.get('email', '').strip(),
            'password': password_encriptada
        }
        
        # Crear el usuario
        usuario_id = Usuario.crear_usuario(data)
        
        if not usuario_id:
            flash("Error al crear el usuario. Intenta nuevamente.", "registro")
            return redirect('/')
    
    except Exception as e:
        flash("Error en el registro. Verifica los datos e intenta nuevamente.", "registro")
        return redirect('/')
    
    # Guardar en sesión
    session['usuario_id'] = usuario_id
    session['nombre'] = request.form['nombre']
    
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    try:
        # Validar credenciales
        if not Usuario.validar_login(request.form):
            return redirect('/')
        
        # Obtener usuario por email (pasar solo el email)
        email = request.form.get('email', '').strip()
        data = {'email': email}
        usuario = Usuario.obtener_por_email(data)
        
        if not usuario:
            flash("Credenciales incorrectas.", "login")
            return redirect('/')
    
    except Exception as e:
        flash("Error en el login. Intenta nuevamente.", "login")
        return redirect('/')
    
    # Guardar en sesión
    session['usuario_id'] = usuario.id
    session['nombre'] = usuario.nombre
    
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')
    
    # Importar aquí para evitar import circular
    from flask_app.models.pelicula import Pelicula
    peliculas = Pelicula.obtener_todas()
    
    return render_template('dashboard.html', peliculas=peliculas)