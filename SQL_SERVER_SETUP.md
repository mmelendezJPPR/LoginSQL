# Guía para Conectar a SQL Server

Para conectar la aplicación a un servidor de SQL Server de Microsoft, sigue estos pasos:

## 1. Instalar el driver ODBC para SQL Server

### En Windows:
1. Descarga e instala "Microsoft ODBC Driver for SQL Server" desde:
   https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

### En Linux:
```bash
# Ubuntu
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
apt-get install -y msodbcsql17
```

## 2. Instalar el paquete pyodbc

```bash
pip install pyodbc
```

## 3. Configurar la conexión a SQL Server

Edita el archivo `config.py` y cambia las siguientes líneas:

```python
# Tipo de base de datos: 'sqlite' o 'mssql'
DB_TYPE = 'mssql'

# Para MS SQL Server: Cadena de conexión
MSSQL_CONNECTION_STRING = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=tu_servidor;DATABASE=tu_base_de_datos;UID=tu_usuario;PWD=tu_contraseña'
```

## 4. Estructura de la base de datos SQL Server

Si estás creando la base de datos desde cero, ejecuta estos comandos en SQL Server Management Studio:

```sql
-- Crear la base de datos
CREATE DATABASE nombre_db;
GO

USE nombre_db;
GO

-- Crear tabla de usuarios
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) UNIQUE NOT NULL,
    password NVARCHAR(255) NOT NULL,
    last_login DATETIME,
    failed_attempts INT DEFAULT 0,
    is_active BIT DEFAULT 1
);
GO

-- Crear tabla de logs de acceso
CREATE TABLE access_logs (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50),
    access_time DATETIME DEFAULT GETDATE(),
    success BIT,
    ip_address NVARCHAR(50),
    user_agent NVARCHAR(255)
);
GO

-- Crear usuario administrador (la aplicación hará el hash de la contraseña)
INSERT INTO users (username, password, is_active)
VALUES ('admin', 'se_reemplazará_por_hash', 1);
GO
```

## 5. Prueba de la conexión

Ejecuta la aplicación y visita la ruta `/test_db` para verificar que la conexión sea exitosa.
