

# ====================================================================
# 🎬 CINEPEDIA - App
# ====================================================================
from flask_app import app

if __name__ == "__main__":
    print("🎬 Iniciando CinePedia...")
    print("💡 Base de datos configurada: CinePediamadeline")
    print("🌐 Servidor ejecutándose en: http://localhost:5037")# 50 + el numero de lista que seria 37
    print("🔧 Modo debug: Activado")
    print("=" * 50)
    
    # Ejecutar la aplicación Flask en modo debug
    app.run(
        host="0.0.0.0",  # Permitir acceso desde cualquier IP
        port=5037,       # Puerto mas el numero de lista (5000 + 37)
        debug=True      
    )