# Plataforma de Clases de Natación

Una plataforma web educativa desarrollada con Django para la gestión y seguimiento de cursos de natación en línea. Permite a los usuarios registrarse, acceder a cursos secuenciales con contenido de video, completar cuestionarios y realizar un seguimiento de su progreso.

## Características

### Gestión de Usuarios
- Sistema completo de autenticación (registro, inicio de sesión, cierre de sesión)
- Recuperación de contraseña mediante correo electrónico
- Redirección automática a registro cuando el usuario no existe
- Perfiles de usuario con seguimiento de progreso

### Sistema de Cursos
- Cursos secuenciales con desbloqueo progresivo
- Contenido de video embebido (URLs almacenadas externamente)
- Sistema de progreso individual por usuario
- Ordenamiento configurable de cursos

### Evaluación y Retroalimentación
- Cuestionarios de opción múltiple por curso
- Calificación automática con 70% de aprobación mínima
- Sistema de feedback para cada curso (comentarios únicos por usuario)
- Seguimiento de resultados históricos

### Calendario de Eventos
- Visualización mensual de eventos
- Navegación entre meses
- Destacado del día actual
- Gestión de eventos relacionados con clases

## Stack Tecnológico

- **Framework:** Django 4.2.27
- **Lenguaje:** Python 3.x
- **Base de Datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Servidor:** Gunicorn (producción)
- **Archivos Estáticos:** WhiteNoise
- **Frontend:** HTML5, CSS, JavaScript

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Virtualenv (recomendado)
- PostgreSQL (para producción)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/plataforma_clases_natacion.git
cd plataforma_clases_natacion
```

### 2. Crear y activar entorno virtual

**Windows:**
```bash
python -m venv env
env\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en el directorio raíz (opcional pero recomendado para producción):

```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,tu-dominio.com
DATABASE_URL=postgres://usuario:contraseña@localhost:5432/nombre_bd
```

### 5. Configurar la base de datos

```bash
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Recolectar archivos estáticos

```bash
python manage.py collectstatic
```

### 8. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

Visita `http://localhost:8000` en tu navegador.

## Estructura del Proyecto

```
plataforma_clases_natacion/
│
├── cursos/                      # App de gestión de cursos
│   ├── migrations/              # Migraciones de BD
│   ├── templates/cursos/        # Plantillas de cursos
│   ├── admin.py                 # Configuración del admin
│   ├── forms.py                 # Formularios
│   ├── models.py                # Modelos (Curso, Pregunta, etc.)
│   ├── urls.py                  # URLs de la app
│   └── views.py                 # Vistas y lógica
│
├── usuarios/                    # App de gestión de usuarios
│   ├── migrations/              # Migraciones de BD
│   ├── admin.py                 # Configuración del admin
│   ├── forms.py                 # Formularios de auth
│   ├── models.py                # Modelo de Perfil
│   ├── signals.py               # Señales de Django
│   ├── urls.py                  # URLs de la app
│   └── views.py                 # Vistas de autenticación
│
├── plataforma_cursos_natacion/  # Configuración principal
│   ├── settings.py              # Configuración de Django
│   ├── urls.py                  # URLs principales
│   └── wsgi.py                  # Configuración WSGI
│
├── templates/                   # Plantillas globales
│   ├── registration/            # Plantillas de recuperación
│   ├── base.html                # Plantilla base
│   ├── dashboard.html           # Dashboard principal
│   ├── login.html               # Página de login
│   └── registro.html            # Página de registro
│
├── static/                      # Archivos estáticos (CSS, JS, imgs)
├── videos/                      # Archivos .txt con URLs de videos
├── manage.py                    # Script de gestión de Django
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Este archivo
```

## Uso

### Panel de Administración

1. Accede a `http://localhost:8000/admin`
2. Inicia sesión con las credenciales del superusuario
3. Gestiona cursos, preguntas, opciones, eventos y usuarios

### Agregar un Curso

1. En el admin, crea un nuevo **Curso**
2. Define: título, descripción, orden y archivo de video
3. Crea **Preguntas** asociadas al curso
4. Agrega **Opciones** para cada pregunta (marca las correctas)

### Configurar Videos

Los videos se almacenan como URLs externas:

1. Crea un archivo `.txt` en la carpeta `videos/` (ej: `video1.txt`)
2. Pega la URL del video embebido (YouTube, Vimeo, etc.)
3. Asocia el archivo al curso en el campo `archivo_video`

Ejemplo de `video1.txt`:
```
https://www.youtube.com/embed/VIDEO_ID
```

### Flujo del Usuario

1. **Registro/Login** → El usuario crea una cuenta o inicia sesión
2. **Dashboard** → Vista principal con acceso a cursos y calendario
3. **Lista de Cursos** → Cursos disponibles (desbloqueados secuencialmente)
4. **Detalle de Curso** → Visualización del video
5. **Cuestionario** → Evaluación del curso (70% para aprobar)
6. **Feedback** → Comentario opcional sobre el curso
7. **Calendario** → Visualización de eventos programados

## Configuración de Producción

### Configurar WhiteNoise (Archivos Estáticos)

Ya está configurado en `settings.py`:
```python
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ...
]
```

### Configurar Gunicorn

```bash
gunicorn plataforma_cursos_natacion.wsgi:application --bind 0.0.0.0:8000
```

### Variables de Entorno Importantes

- `SECRET_KEY`: Clave secreta de Django (debe ser única)
- `DEBUG`: Debe ser `False` en producción
- `ALLOWED_HOSTS`: Dominios permitidos
- `DATABASE_URL`: URL de conexión a PostgreSQL

## Modelos de Datos

### Curso
- `titulo`: Nombre del curso
- `descripcion`: Descripción detallada
- `orden`: Número de orden (para secuencia)
- `archivo_video`: Nombre del archivo .txt con URL

### ProgresoCurso
- `usuario`: Relación con User
- `curso`: Relación con Curso
- `completado`: Estado de finalización

### Pregunta
- `curso`: Curso asociado
- `texto`: Enunciado de la pregunta

### Opcion
- `pregunta`: Pregunta asociada
- `texto`: Texto de la opción
- `es_correcta`: Marca si es la respuesta correcta

### ResultadoCuestionario
- `usuario`: Usuario que realizó el cuestionario
- `curso`: Curso evaluado
- `correctas`: Número de respuestas correctas
- `incorrectas`: Número de respuestas incorrectas
- `aprobado`: Estado de aprobación

### Feedback
- `usuario`: Usuario que comenta
- `curso`: Curso comentado
- `comentario`: Texto del feedback
- `fecha`: Fecha de creación

### Evento
- `titulo`: Nombre del evento
- `descripcion`: Descripción del evento
- `fecha`: Fecha del evento

## Contribuir

1. Haz un fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Realiza tus cambios y haz commit (`git commit -m 'Agrega nueva funcionalidad'`)
4. Sube tus cambios (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Seguridad

- Cambia el `SECRET_KEY` en producción
- Nunca subas credenciales al repositorio
- Usa variables de entorno para datos sensibles
- Configura `DEBUG = False` en producción
- Implementa HTTPS en producción
- Configura `ALLOWED_HOSTS` correctamente

## Licencia

Este proyecto es de código abierto. Consulta el archivo LICENSE para más detalles.

## Soporte

Para reportar problemas o sugerencias, abre un issue en el repositorio de GitHub.

## Autor

Desarrollado para la gestión de cursos de natación en línea.
