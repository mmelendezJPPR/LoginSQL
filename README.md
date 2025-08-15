# Sistema de Login - Junta de Planificación

Sistema de autenticación para la Junta de Planificación.

## Configuración para desarrollo local

1. Clonar el repositorio:
```bash
git clone https://github.com/mmelendezJPPR/LoginSQL.git
cd LoginSQL
```

2. Crear un entorno virtual e instalar dependencias:
```bash
python -m venv .venv
.venv\Scripts\activate  # En Windows
pip install -r requirements.txt
```

3. Copiar el archivo `.env.example` a `.env` y configurar las variables:
```bash
copy .env.example .env
# Editar el archivo .env con las credenciales correctas
```

4. Ejecutar la aplicación:
```bash
python app.py
```

## Despliegue en Render

Esta aplicación está configurada para desplegarse en Render. En el entorno de Render, se usará una base de datos SQLite con datos de demostración en lugar de conectarse a la base de datos SQL Server corporativa.

### Variables de entorno para Render:

- `SECRET_KEY`: Clave secreta para la aplicación Flask
- `RENDER`: Establecer a `True` para activar el modo de demostración
- `PORT`: Puerto para la aplicación (generalmente proporcionado por Render)

### Usuarios de demostración:

- Usuario: `demo`, Contraseña: `demo123`
- Usuario: `admin`, Contraseña: `admin456`

## Notas de seguridad

- La versión desplegada en Render es SOLO PARA DEMOSTRACIÓN y usa datos ficticios
- Para el entorno de producción, se recomienda usar contraseñas con hash y conexiones seguras
- Nunca suba credenciales de base de datos al repositorio
