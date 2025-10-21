from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

DATABASE = 'CinePediamadeline'

class Comentario:
    def __init__(self, data):
        self.id = data['id']
        self.comentario = data['comentario']
        self.usuario_id = data['usuario_id']
        self.pelicula_id = data['pelicula_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Método para crear un nuevo comentario
    @classmethod
    def crear_comentario(cls, data):
        query = """
        INSERT INTO comentarios (comentario, usuario_id, pelicula_id)
        VALUES (%(comentario)s, %(usuario_id)s, %(pelicula_id)s)
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    # Método para obtener comentarios de una película (más reciente primero)
    @classmethod
    def obtener_por_pelicula(cls, pelicula_id):
        query = """
        SELECT c.*, u.nombre, u.apellido 
        FROM comentarios c 
        LEFT JOIN usuarios u ON c.usuario_id = u.id 
        WHERE c.pelicula_id = %(pelicula_id)s
        ORDER BY c.created_at DESC
        """
        data = {'pelicula_id': pelicula_id}
        resultados = connectToMySQL(DATABASE).query_db(query, data)
        comentarios = []
        if resultados:
            for comentario in resultados:
                comentarios.append(comentario)
        return comentarios

    # Método para eliminar un comentario
    @classmethod
    def eliminar_comentario(cls, data):
        query = "DELETE FROM comentarios WHERE id = %(id)s AND usuario_id = %(usuario_id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    # Validar comentario
    @staticmethod
    def validar_comentario(data):
        is_valid = True
        
        # Validar que el comentario tenga al menos 3 caracteres
        if len(data['comentario']) < 3:
            flash("El comentario debe tener al menos 3 caracteres.", "comentario")
            is_valid = False
        
        return is_valid