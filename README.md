# 🎬 CINEPEDIA - Sistema de Gestión de Películas

## ✨ NUEVO DISEÑO MORADO-NEGRO DINÁMICO ✨

### 🎨 Características del Diseño:

#### 🌟 **Efectos Visuales Únicos:**
- **Degradado Animado:** Fondo con transición automática morado-negro
- **Glassmorphism:** Tarjetas con efecto cristal y blur
- **Animaciones Flotantes:** Elementos con movimiento suave
- **Efectos de Hover:** Transformaciones 3D y brillos neón
- **Partículas de Fondo:** Efectos lumínicos dinámicos

#### 🎯 **Elementos Interactivos:**
- **Botones Animados:** Con efectos de brillo y transformación
- **Formularios Futuristas:** Bordes neón y efectos de focus
- **Navbar Cristal:** Con blur y transparencia
- **Cards Flotantes:** Con sombras dinámicas y efectos 3D
- **Scrollbar Personalizado:** Con gradiente morado

#### 🌈 **Paleta de Colores:**
```css
--primary-purple: #6a0dad
--secondary-purple: #9b59b6  
--dark-purple: #4a0e4e
--deep-black: #1a1a1a
--neon-purple: #bf00ff
--light-purple: #e8d5ff
```

## 🚀 Instalación y Uso

### 1. **Activar Entorno Virtual:**
```bash
venv\Scripts\activate
```

### 2. **Crear Base de Datos:**
```sql
mysql -u root -padmin4B < base.sql
```

### 3. **Ejecutar Aplicación:**
```bash
python server.py
```

### 4. **Acceder a la App:**
```
http://localhost:5000
```

## 📱 Funcionalidades de la App

### ✅ **Sistema de Usuario:**
- Registro con validación completa
- Login seguro con bcrypt
- Sesiones protegidas

### ✅ **Gestión de Películas:**
- Crear películas (solo propietarios)
- Ver catálogo completo
- Editar información (solo propietarios)  
- Eliminar películas (solo propietarios)
- Títulos únicos (BONUS)

### ✅ **Sistema de Comentarios:**
- Agregar comentarios a cualquier película
- Ver comentarios con autor y fecha
- Sistema de timestamps

### ✅ **Validaciones Avanzadas:**
- Campos mínimo 3 caracteres
- Años válidos (1880-2025)
- Emails únicos
- Formularios con persistencia de datos (BONUS)

## 🛠️ Tecnologías

- **Backend:** Flask 2.3.2 + Python 3.13.5
- **Base de Datos:** MySQL + PyMySQL 1.1.0  
- **Autenticación:** Flask-Bcrypt 1.0.1
- **Frontend:** Bootstrap 5 + CSS3 Avanzado
- **Arquitectura:** MVC Profesional

## 🎮 Estructura del Proyecto

```
certificacion_2/
├── 📄 server.py                    # Entrada principal
├── 📄 base.sql                     # Script MySQL único
├── 📂 flask_app/
│   ├── 📄 __init__.py             # Flask + Bcrypt
│   ├── 📂 config/
│   │   └── 📄 mysqlconnection.py  # Conexión DB
│   ├── 📂 models/                 # Lógica de datos
│   ├── 📂 controllers/            # Rutas y controladores  
│   ├── 📂 templates/              # Vistas HTML
│   └── 📂 static/css/
│       └── 📄 style.css           # 🎨 DISEÑO PERSONALIZADO
└── 📂 venv/                       # Entorno virtual
```

## 🎨 Efectos CSS Implementados

### 🌟 **Animaciones:**
- `gradientShift`: Degradado de fondo animado
- `floatAnimation`: Elementos flotantes
- `pulseGlow`: Efecto de brillo pulsante
- `fadeInUp`: Aparición suave de elementos

### 💎 **Efectos Especiales:**
- **Glassmorphism:** Transparencias con blur
- **Transformaciones 3D:** Rotaciones y escalas en hover
- **Sombras Dinámicas:** Con colores neón
- **Gradientes Animados:** Backgrounds que cambian
- **Efectos de Partículas:** Fondo con luces flotantes

## 🌐 Vista Previa del Diseño

El nuevo diseño incluye:
- ✨ **Fondo animado** con degradado morado-negro
- 💜 **Efectos neón** en botones y elementos interactivos  
- 🔮 **Tarjetas cristal** con transparencia y blur
- 🎭 **Animaciones suaves** en todos los elementos
- 📱 **Diseño responsive** para móviles
- 🎨 **Paleta coherente** morado-negro futurista

---

## 🎯 Estado del Proyecto: 

🟢 **COMPLETAMENTE FUNCIONAL**  
🎨 **DISEÑO PERSONALIZADO ÚNICO**  
⚡ **EFECTOS DINÁMICOS IMPLEMENTADOS**  
📱 **RESPONSIVE Y MODERNO**

**¡Disfruta de CinePedia con su nuevo look futurista! 🎬💜**