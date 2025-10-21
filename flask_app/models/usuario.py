from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app import bcrypt

DATABASE = 'CinePediamadeline'

class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Método para crear un nuevo usuario
    @classmethod
    def crear_usuario(cls, data):
        query = """
        INSERT INTO usuarios (nombre, apellido, email, password)
        VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s)
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    # Método para obtener un usuario por email
    @classmethod
    def obtener_por_email(cls, data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s"
        resultado = connectToMySQL(DATABASE).query_db(query, data)
        
        # Verificar que el resultado no sea False (error) y que tenga datos
        if not resultado or len(resultado) < 1:
            return False
        return cls(resultado[0])

    # Método para obtener un usuario por ID
    @classmethod
    def obtener_por_id(cls, data):
        query = "SELECT * FROM usuarios WHERE id = %(id)s"
        resultado = connectToMySQL(DATABASE).query_db(query, data)
        
        # Verificar que el resultado no sea False (error) y que tenga datos
        if not resultado or len(resultado) < 1:
            return False
        return cls(resultado[0])

    # Método para obtener todos los usuarios
    @classmethod
    def obtener_todos(cls):
        query = "SELECT * FROM usuarios"
        resultados = connectToMySQL(DATABASE).query_db(query)
        usuarios = []
        for usuario in resultados:
            usuarios.append(cls(usuario))
        return usuarios

    # Validaciones
    @staticmethod
    def validar_registro(data):
        is_valid = True
        
        # Validar que los campos existan y no estén vacíos
        if 'nombre' not in data or not data['nombre'] or len(data['nombre'].strip()) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "registro")
            is_valid = False
        
        if 'apellido' not in data or not data['apellido'] or len(data['apellido'].strip()) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "registro")
            is_valid = False
        
        # Validar email
        if 'email' not in data or not data['email']:
            flash("El email es requerido.", "registro")
            is_valid = False
        else:
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(data['email']):
                flash("Formato de email inválido.", "registro")
                is_valid = False
            else:
                # Verificar si el email ya existe
                email_data = {'email': data['email']}
                if Usuario.obtener_por_email(email_data):
                    flash("El email ya está registrado.", "registro")
                    is_valid = False
        
        # Validar contraseña (reducido a 6 caracteres para compatibilidad)
        if 'password' not in data or not data['password'] or len(data['password']) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "registro")
            is_valid = False
        
        # Confirmar contraseña
        if 'confirm_password' not in data or data['password'] != data['confirm_password']:
            flash("Las contraseñas no coinciden.", "registro")
            is_valid = False
        
        return is_valid

    @staticmethod
    def validar_login(data):
        is_valid = True
        
        # Validar que los campos existan
        if 'email' not in data or not data['email']:
            flash("El email es requerido.", "login")
            return False
        
        if 'password' not in data or not data['password']:
            flash("La contraseña es requerida.", "login")
            return False
        
        # Crear el diccionario con el email para la consulta
        email_data = {'email': data['email']}
        
        # Verificar email
        usuario = Usuario.obtener_por_email(email_data)
        if not usuario:
            flash("Email/Contraseña incorrectos.", "login")
            is_valid = False
        elif not bcrypt.check_password_hash(usuario.password, data['password']):
            flash("Email/Contraseña incorrectos.", "login")
            is_valid = False
        
        return is_valid