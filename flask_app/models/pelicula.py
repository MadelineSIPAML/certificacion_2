from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

DATABASE = 'CinePediamadeline'

class Pelicula:
    def __init__(self, data):
        self.id = data['id']
        self.titulo = data['titulo']
        self.director = data['director']
        self.genero = data['genero']
        self.anio = data['anio']
        self.sinopsis = data['sinopsis']
        self.usuario_id = data['usuario_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Método para crear una nueva película
    @classmethod
    def crear_pelicula(cls, data):
        query = """
        INSERT INTO peliculas (titulo, director, genero, anio, sinopsis, usuario_id)
        VALUES (%(titulo)s, %(director)s, %(genero)s, %(anio)s, %(sinopsis)s, %(usuario_id)s)
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    # Método para obtener todas las películas
    @classmethod
    def obtener_todas(cls):
        query = """
        SELECT p.*, u.nombre, u.apellido 
        FROM peliculas p 
        LEFT JOIN usuarios u ON p.usuario_id = u.id
        ORDER BY p.created_at DESC
        """
        resultados = connectToMySQL(DATABASE).query_db(query)
        peliculas = []
        for pelicula in resultados:
            peliculas.append(pelicula)  # Devolvemos el diccionario completo con datos del usuario
        return peliculas

    # Método para obtener una película por ID
    @classmethod
    def obtener_por_id(cls, data):
        query = """
        SELECT p.*, u.nombre, u.apellido 
        FROM peliculas p 
        LEFT JOIN usuarios u ON p.usuario_id = u.id 
        WHERE p.id = %(id)s
        """
        resultado = connectToMySQL(DATABASE).query_db(query, data)
        
        # Verificar que el resultado no sea False (error) y que tenga datos
        if not resultado or len(resultado) < 1:
            return False
        return resultado[0]  # Devolvemos el diccionario completo

    # Método para obtener películas de un usuario específico
    @classmethod
    def obtener_por_usuario(cls, data):
        query = """
        SELECT p.*, u.nombre, u.apellido 
        FROM peliculas p 
        LEFT JOIN usuarios u ON p.usuario_id = u.id 
        WHERE p.usuario_id = %(usuario_id)s
        ORDER BY p.created_at DESC
        """
        resultados = connectToMySQL(DATABASE).query_db(query, data)
        peliculas = []
        for pelicula in resultados:
            peliculas.append(pelicula)
        return peliculas

    # Método para actualizar una película
    @classmethod
    def actualizar_pelicula(cls, data):
        query = """
        UPDATE peliculas 
        SET titulo = %(titulo)s, director = %(director)s, genero = %(genero)s, 
            anio = %(anio)s, sinopsis = %(sinopsis)s
        WHERE id = %(id)s AND usuario_id = %(usuario_id)s
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    # Método para eliminar una película
    @classmethod
    def eliminar_pelicula(cls, data):
        query = "DELETE FROM peliculas WHERE id = %(id)s AND usuario_id = %(usuario_id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    # Método para verificar si un título ya existe
    @classmethod
    def titulo_existe(cls, titulo, pelicula_id=None):
        if pelicula_id:
            # Para edición, excluir la película actual
            query = "SELECT * FROM peliculas WHERE titulo = %(titulo)s AND id != %(id)s"
            data = {'titulo': titulo, 'id': pelicula_id}
        else:
            # Para creación nueva
            query = "SELECT * FROM peliculas WHERE titulo = %(titulo)s"
            data = {'titulo': titulo}
        
        resultado = connectToMySQL(DATABASE).query_db(query, data)
        return resultado and len(resultado) > 0

    # Validaciones
    @staticmethod
    def validar_pelicula(data, pelicula_id=None):
        is_valid = True
        
        try:
            # Validar título (mínimo 3 caracteres)
            if 'titulo' not in data or not data['titulo'] or len(data['titulo'].strip()) < 3:
                flash("El título debe tener al menos 3 caracteres.", "pelicula")
                is_valid = False
            
            # BONUS: Validar que el título sea único (solo si título es válido)
            elif 'titulo' in data and data['titulo']:
                if Pelicula.titulo_existe(data['titulo'], pelicula_id):
                    flash("Ya existe una película con este título.", "pelicula")
                    is_valid = False
            
            # Validar director (mínimo 3 caracteres)
            if 'director' not in data or not data['director'] or len(data['director'].strip()) < 3:
                flash("El director debe tener al menos 3 caracteres.", "pelicula")
                is_valid = False
            
            # Validar género (mínimo 3 caracteres)
            if 'genero' not in data or not data['genero'] or len(data['genero'].strip()) < 3:
                flash("Debe seleccionar un género.", "pelicula")
                is_valid = False
        
        except RuntimeError:
            # No estamos en contexto Flask, validación básica
            if 'titulo' not in data or not data['titulo'] or len(data['titulo'].strip()) < 3:
                is_valid = False
            if 'director' not in data or not data['director'] or len(data['director'].strip()) < 3:
                is_valid = False
            if 'genero' not in data or not data['genero'] or len(data['genero'].strip()) < 3:
                is_valid = False
        
        try:
            # Validar año
            if 'anio' not in data or not data['anio']:
                flash("El año es requerido.", "pelicula")
                is_valid = False
            else:
                try:
                    anio = int(data['anio'])
                    if anio < 1880 or anio > 2025:
                        flash("El año debe estar entre 1880 y 2025.", "pelicula")
                        is_valid = False
                except ValueError:
                    flash("El año debe ser un número válido.", "pelicula")
                    is_valid = False
            
            # Validar sinopsis (mínimo 3 caracteres)
            if 'sinopsis' not in data or not data['sinopsis'] or len(data['sinopsis'].strip()) < 3:
                flash("La sinopsis debe tener al menos 3 caracteres.", "pelicula")
                is_valid = False
            
        except RuntimeError:
            # No estamos en contexto Flask
            if 'anio' not in data or not data['anio']:
                is_valid = False
            else:
                try:
                    anio = int(data['anio'])
                    if anio < 1880 or anio > 2025:
                        is_valid = False
                except ValueError:
                    is_valid = False
            
            if 'sinopsis' not in data or not data['sinopsis'] or len(data['sinopsis'].strip()) < 3:
                is_valid = False
        
        return is_valid