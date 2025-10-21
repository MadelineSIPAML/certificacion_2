-- ===================================================
-- 🎬 CINEPEDIA - BASE DE DATOS COMPLETA Y OPTIMIZADA
-- ===================================================
-- Sistema de gestión de películas con comentarios
-- Compatible con Flask, PyMySQL y validaciones completas
-- ===================================================

-- Eliminar y crear la base de datos
DROP DATABASE IF EXISTS CinePediamadeline;
CREATE DATABASE CinePediamadeline CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE CinePediamadeline;

-- ===================================================
-- TABLA USUARIOS - Sistema de autenticación
-- ===================================================
CREATE TABLE usuarios(
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(45) NOT NULL COMMENT 'Nombre del usuario (mínimo 3 caracteres)',
    apellido VARCHAR(45) NOT NULL COMMENT 'Apellido del usuario (mínimo 3 caracteres)',
    email VARCHAR(255) UNIQUE NOT NULL COMMENT 'Email único del usuario',
    password VARCHAR(255) NOT NULL COMMENT 'Contraseña hasheada con bcrypt',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Índices para optimización
    INDEX idx_email (email),
    INDEX idx_nombre_apellido (nombre, apellido)
) ENGINE=InnoDB COMMENT='Tabla de usuarios del sistema';

-- ===================================================
-- TABLA PELICULAS - Gestión de películas
-- ===================================================
CREATE TABLE peliculas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(255) NOT NULL COMMENT 'Título único de la película (mínimo 3 caracteres)',
    director VARCHAR(255) NOT NULL COMMENT 'Director de la película (mínimo 3 caracteres)',
    genero VARCHAR(100) NOT NULL COMMENT 'Género de la película',
    anio YEAR NOT NULL COMMENT 'Año de estreno (1880-2025)',
    duracion INT DEFAULT NULL COMMENT 'BONUS: Duración en minutos',
    rating DECIMAL(2,1) DEFAULT NULL COMMENT 'BONUS: Calificación promedio (1.0-5.0)',
    poster_url VARCHAR(500) DEFAULT NULL COMMENT 'BONUS: URL del poster de la película',
    sinopsis TEXT NOT NULL COMMENT 'Sinopsis de la película (mínimo 3 caracteres)',
    usuario_id INT NOT NULL COMMENT 'ID del usuario que creó la película',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Restricciones
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    UNIQUE KEY unique_titulo (titulo) COMMENT 'BONUS: Títulos únicos',
    
    -- Índices para optimización
    INDEX idx_titulo (titulo),
    INDEX idx_usuario_id (usuario_id),
    INDEX idx_genero (genero),
    INDEX idx_anio (anio),
    INDEX idx_rating (rating DESC) COMMENT 'BONUS: Para ordenar por mejor calificación',
    INDEX idx_created_at (created_at DESC),
    FULLTEXT INDEX idx_fulltext_search (titulo, sinopsis) COMMENT 'BONUS: Búsqueda de texto completo'
) ENGINE=InnoDB COMMENT='Tabla de películas con títulos únicos y características BONUS';

-- ===================================================
-- TABLA COMENTARIOS - Sistema de comentarios BONUS
-- ===================================================
CREATE TABLE comentarios(
    id INT PRIMARY KEY AUTO_INCREMENT,
    comentario TEXT NOT NULL COMMENT 'Contenido del comentario (mínimo 3 caracteres)',
    usuario_id INT NOT NULL COMMENT 'ID del usuario que escribió el comentario',
    pelicula_id INT NOT NULL COMMENT 'ID de la película comentada',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Restricciones
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY(pelicula_id) REFERENCES peliculas(id) ON DELETE CASCADE,
    
    -- Índices para optimización
    INDEX idx_pelicula_id (pelicula_id),
    INDEX idx_usuario_id (usuario_id),
    INDEX idx_created_at (created_at DESC) COMMENT 'Para ordenar comentarios por más reciente'
) ENGINE=InnoDB COMMENT='BONUS: Comentarios de películas ordenados por fecha';

-- ===================================================
-- VERIFICACIÓN DE TABLAS CREADAS
-- ===================================================
SHOW TABLES;
DESCRIBE usuarios;
DESCRIBE peliculas;
DESCRIBE comentarios;

-- ===================================================
-- DATOS DE PRUEBA PARA TESTING
-- ===================================================

-- Usuarios de ejemplo con contraseñas hasheadas
INSERT INTO usuarios (nombre, apellido, email, password) VALUES 
('Administrador', 'CinePedia', 'admin@cinepedia.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdnBC7EvOA.kX.K'),
('María', 'García', 'maria@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdnBC7EvOA.kX.K'),
('Juan', 'Pérez', 'juan@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdnBC7EvOA.kX.K');

-- Películas de ejemplo con títulos únicos y características BONUS
INSERT INTO peliculas (titulo, director, genero, anio, duracion, rating, poster_url, sinopsis, usuario_id) VALUES 
('El Padrino', 'Francis Ford Coppola', 'Drama', 1972, 175, 4.9, 'https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg', 'La historia épica de una familia de la mafia italiana en Nueva York, considerada una de las mejores películas de todos los tiempos.', 1),
('Interestelar', 'Christopher Nolan', 'Ciencia Ficción', 2014, 169, 4.6, 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg', 'Un grupo de exploradores viaja a través de un agujero de gusano en el espacio en un intento de asegurar la supervivencia de la humanidad.', 2),
('Perdido', 'David Fincher', 'Thriller', 2014, 149, 4.2, 'https://image.tmdb.org/t/p/w500/2Ah63TIvVmZM3hzUwR5hXFg2LEk.jpg', 'Con la desaparición de su esposa el día de su quinto aniversario de bodas, Nick Dunne se convierte en el principal sospechoso.', 3);

-- Comentarios de ejemplo (BONUS)
INSERT INTO comentarios (comentario, usuario_id, pelicula_id) VALUES 
('Una obra maestra absoluta del cine. Las actuaciones son excepcionales y la dirección es perfecta.', 2, 1),
('Me encantó esta película! La ciencia ficción nunca había sido tan emocional.', 3, 2),
('Increíble thriller psicológico. Te mantiene en tensión hasta el final.', 1, 3),
('No puedo creer que se estrenara hace 10 años, sigue siendo relevante.', 1, 2);

-- ===================================================
-- CONSULTAS DE VERIFICACIÓN
-- ===================================================
SELECT 'Verificando datos insertados...' AS status;

SELECT COUNT(*) AS total_usuarios FROM usuarios;
SELECT COUNT(*) AS total_peliculas FROM peliculas;
SELECT COUNT(*) AS total_comentarios FROM comentarios;

-- Mostrar películas con sus creadores y características BONUS
SELECT p.titulo, p.director, p.genero, p.anio, p.duracion, p.rating,
       CONCAT(u.nombre, ' ', u.apellido) AS creado_por
FROM peliculas p 
JOIN usuarios u ON p.usuario_id = u.id
ORDER BY p.rating DESC;

-- BONUS: Consulta de búsqueda de texto completo
SELECT p.titulo, p.director, p.sinopsis, p.rating,
       MATCH(titulo, sinopsis) AGAINST('familia historia' IN NATURAL LANGUAGE MODE) AS relevancia
FROM peliculas p 
WHERE MATCH(titulo, sinopsis) AGAINST('familia historia' IN NATURAL LANGUAGE MODE)
ORDER BY relevancia DESC;

-- BONUS: Estadísticas de películas por género
SELECT genero, 
       COUNT(*) AS total_peliculas,
       AVG(rating) AS rating_promedio,
       AVG(duracion) AS duracion_promedio
FROM peliculas 
WHERE rating IS NOT NULL 
GROUP BY genero
ORDER BY rating_promedio DESC;

-- Mostrar comentarios con información completa
SELECT c.comentario, 
       CONCAT(u.nombre, ' ', u.apellido) AS comentado_por,
       p.titulo AS pelicula,
       c.created_at
FROM comentarios c
JOIN usuarios u ON c.usuario_id = u.id
JOIN peliculas p ON c.pelicula_id = p.id
ORDER BY c.created_at DESC;

-- ===================================================
-- CONFIGURACIÓN FINAL Y VERIFICACIONES BONUS
-- ===================================================
SELECT 'Base de datos CinePediamadeline configurada correctamente!' AS mensaje;
SELECT 'Sistema listo para funcionar con todas las características BONUS' AS bonus;

-- BONUS: Verificación de índices creados
SHOW INDEX FROM peliculas WHERE Key_name LIKE 'idx_%' OR Key_name LIKE '%fulltext%';

-- BONUS: Verificación de constraints UNIQUE
SELECT CONSTRAINT_NAME, COLUMN_NAME, TABLE_NAME 
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
WHERE TABLE_SCHEMA = 'CinePediamadeline' 
AND CONSTRAINT_NAME LIKE '%unique%';

-- BONUS: Conteo final con nuevos campos
SELECT 'RESUMEN FINAL DE LA BASE DE DATOS:' AS titulo;
SELECT COUNT(*) AS total_usuarios FROM usuarios;
SELECT COUNT(*) AS total_peliculas FROM peliculas;
SELECT COUNT(*) AS total_comentarios FROM comentarios;
SELECT COUNT(*) AS peliculas_con_rating FROM peliculas WHERE rating IS NOT NULL;
SELECT COUNT(*) AS peliculas_con_poster FROM peliculas WHERE poster_url IS NOT NULL;