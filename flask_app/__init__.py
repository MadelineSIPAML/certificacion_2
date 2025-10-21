from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "clave_secreta_super_segura"  # Cambia esto por una clave más segura

# Inicializar bcrypt
bcrypt = Bcrypt(app)

# Importar controladores debe ir al final para evitar imports circulares
from flask_app.controllers import usuarios, peliculas, comentarios