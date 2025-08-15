# Configuración de la Base de Datos

# Tipo de base de datos: 'sqlite' o 'mssql'
# Por defecto usa 'sqlite' que es más sencillo para desarrollo
DB_TYPE = 'sqlite'

# Para SQLite: Nombre del archivo de base de datos
SQLITE_FILE = 'users.db'

# Para MS SQL Server: Cadena de conexión
# Ejemplo: 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=myserver;DATABASE=mydatabase;UID=myusername;PWD=mypassword'
MSSQL_CONNECTION_STRING = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=myserver;DATABASE=mydatabase;UID=myusername;PWD=mypassword'

# Configuración de la aplicación Flask
SECRET_KEY = 'cambia_esto_a_una_clave_secreta_segura'  # Usar una clave segura en producción
FLASK_HOST = '0.0.0.0'  # Escucha en todas las interfaces
FLASK_PORT = 5000
FLASK_DEBUG = True  # Cambiar a False en producción

# Configuración de logging
LOG_LEVEL = 'DEBUG'  # Opciones: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = 'app.log'
