# Gestor de Tutorías Individuales para Profesores

## Descripción
Este proyecto tiene como objetivo proporcionar una plataforma para **gestionar las tutorías individuales** de estudiantes, permitiendo a los profesores registrar, editar y eliminar las tutorías realizadas, así como asociarlas a un estudiante específico. La herramienta también incluye funcionalidades para importar listas de estudiantes desde archivos CSV.

El sistema está construido con **Django**, **Bootstrap**, y **Docker**, siguiendo principios de **gestión pedagógica** y **optimización UX**.

---

## Funcionalidades

1. **Gestión de estudiantes**: 
   - Los profesores pueden **ver, crear, editar y eliminar** estudiantes.
   - Los estudiantes son cargados desde la base de datos o mediante **importación de archivos CSV**.

2. **Gestión de tutorías**: 
   - Los profesores pueden **crear, editar y eliminar** tutorías individuales asociadas a los estudiantes.
   - Cada tutoría contiene los siguientes campos:
     - Estudiante (seleccionable desde una lista desplegable)
     - Fecha
     - Situación trabajada (máximo 25 palabras)
     - Fase motivacional dominante
     - Dimensiones trabajadas (mín. 1, máx. 3)
     - Desarrollo de la sesión (máximo 100 palabras)
     - Meta concreta (máximo 30 palabras)
     - Compromiso del tutor (máximo 30 palabras)
     - Criterio profesional (única opción seleccionable)
     - Observaciones (máximo 40 palabras)

3. **Control de validación**:
   - Los campos de **situación trabajada**, **desarrollo de la sesión**, **meta concreta**, y **compromiso del tutor** están limitados a un máximo de palabras, con mensajes visuales indicando el número de palabras.
   - La selección de **dimensiones trabajadas** está limitada a un máximo de 3 opciones.

4. **Autenticación**:
   - Los usuarios deben **iniciar sesión** para poder registrar y gestionar tutorías.
   - Los estudiantes se filtran según el **profesor logueado**.

5. **Visualización de tutorías**:
   - Los profesores pueden ver un listado de las **tutorías registradas** por estudiante.
   - Los detalles de las tutorías incluyen información como fecha, fase motivacional, situación trabajada, entre otros.

6. **Eliminar tutorías**:
   - Los registros de tutorías pueden ser **eliminados** por el profesor desde la interfaz.

7. **Gestión de cuentas de profesores**:
   - **Los administradores pueden gestionar las cuentas de los profesores** y asignarles permisos específicos a través del panel de administración de Django.
   - Se pueden asignar permisos para **ver, crear, editar o eliminar** tutorías, así como **gestionar los estudiantes** asignados a cada profesor.
   - **Permisos específicos** pueden ser otorgados por el administrador, asegurando que los profesores solo puedan ver los estudiantes y tutorías que les pertenecen.

---

## Estructura del Proyecto
gestor_tutorias/
│
├── app/
│ ├── accounts/
│ ├── config/
│ ├── core/
│ ├── students/
│ ├── tutoring/
│ └── templates/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py


---

## Requisitos

- **Python 3.12** o superior
- **Django 4.2** o superior
- **Docker** (para la ejecución en contenedores)
- **Bootstrap 5** (para la interfaz)
- **Base de datos SQLite** (configurado por defecto, pero se puede usar PostgreSQL o MySQL)

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/gestor_tutorias.git
cd gestor_tutorias
2. Crear un entorno virtual
python3 -m venv venv
source venv/bin/activate  # Para Linux/Mac
venv\Scripts\activate     # Para Windows
3. Instalar dependencias
pip install -r requirements.txt
4. Configurar Docker

Si deseas usar Docker para la ejecución, asegúrate de tener Docker y Docker Compose instalados.

docker-compose up --build

Esto iniciará los contenedores para la base de datos y la aplicación web.

Migraciones y Carga Inicial
Ejecuta las migraciones para preparar la base de datos:
docker-compose run --rm web python manage.py makemigrations
docker-compose run --rm web python manage.py migrate
Crea un superusuario para acceder a la administración:
docker-compose run --rm web python manage.py createsuperuser
Acceso
Accede a la aplicación en el navegador:
http://127.0.0.1:8000
Inicia sesión como superusuario para administrar el sistema.
Panel de Administración de Django
¿Cómo gestionar cuentas de profesores y asignar permisos?
Accede a el panel de administración
.
Inicia sesión con el superusuario que creaste.
En la sección Usuarios, selecciona Usuarios y edita las cuentas de los profesores.
Asigna permisos de acceso a tutorías, estudiantes, etc., y asegúrate de que el profesor tenga acceso solo a sus propios registros de estudiantes y tutorías.
Pruebas

Este proyecto incluye pruebas automatizadas para las vistas, formularios y procesos de creación, edición y eliminación de tutorías. Para ejecutarlas:

docker-compose run --rm web python manage.py test tutoring
Notas
Este proyecto está en constante evolución. Las funcionalidades básicas están implementadas y probadas.
Puedes extender la funcionalidad, por ejemplo, añadiendo notificaciones por correo o exportación a PDF de las tutorías.
Contribuir

Si deseas contribuir, puedes hacer un fork del repositorio y enviar un pull request.

Realiza cambios.
Escribe pruebas para los cambios.
Envía el pull request.
Licencia

Este proyecto está bajo la Licencia MIT.


---

## Cambios Realizados:

- Añadido un **bloque de gestión de cuentas de profesores** en el README para guiar a los administradores sobre cómo manejar las cuentas y permisos.
- Descripción de las funcionalidades básicas y cómo el administrador puede **asignar permisos** específicos a los profesores.
  
### ¿Qué sigue?

- Ejecutar las **pruebas** nuevamente para asegurarnos de que todo funcione correctamente.
- Probar los **flujos de edición y eliminación** en la interfaz para los profesores.

Cuando todo esté en orden, podemos proceder con más mejoras como **exportar los datos a PDF** o **agregar notificaciones por correo**.