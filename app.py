from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
import pyodbc
import logging
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'clave_temporal_segura')

# Configuración de la conexión a SQL Server
SERVER = os.getenv('DB_SERVER', 'localhost')
DATABASE = os.getenv('DB_NAME', 'Test_Users')
USE_WINDOWS_AUTH = os.getenv('DB_WINDOWS_AUTH', 'True').lower() == 'true'
USERNAME = os.getenv('DB_USER', '')
PASSWORD = os.getenv('DB_PASSWORD', '')

# Determinar si estamos en Render
IS_RENDER = os.getenv('RENDER', False)

def get_db_connection():
    """Establece y devuelve una conexión a la base de datos"""
    # Si estamos en Render, usar SQLite para demostración
    if IS_RENDER:
        return get_sqlite_connection()
    else:
        return get_sqlserver_connection()

def get_sqlserver_connection():
    """Conexión a SQL Server (para desarrollo local)"""
    try:
        if USE_WINDOWS_AUTH:
            conn_str = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'
        else:
            conn_str = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
        
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as e:
        logger.error(f"Error al conectar a la base de datos SQL Server: {e}")
        return None

def get_sqlite_connection():
    """Conexión a SQLite (para demostración en Render)"""
    try:
        import sqlite3
        conn = sqlite3.connect('/tmp/demo_users.db')
        conn.row_factory = sqlite3.Row
        
        # Inicializar la base de demostración si no existe
        init_demo_db(conn)
        
        return conn
    except Exception as e:
        logger.error(f"Error al conectar a la base de datos SQLite: {e}")
        return None

def init_demo_db(conn):
    """Inicializa la base de datos SQLite para demostración"""
    cursor = conn.cursor()
    
    # Crear tabla de usuarios si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password_hash TEXT
    )
    ''')
    
    # Insertar usuarios de demostración
    try:
        cursor.execute('INSERT OR IGNORE INTO Users VALUES (1, "demo", "demo123")')
        cursor.execute('INSERT OR IGNORE INTO Users VALUES (2, "admin", "admin456")')
        conn.commit()
    except Exception as e:
        logger.error(f"Error al inicializar datos de demostración: {e}")
        conn.rollback()

# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validación básica
        if not username or not password:
            flash('Por favor ingrese usuario y contraseña', 'error')
            return redirect(url_for('index'))
        
        # Consultar la base de datos
        conn = get_db_connection()
        if conn:
            try:
                if IS_RENDER:
                    # Para SQLite (demostración)
                    cursor = conn.cursor()
                    cursor.execute('SELECT user_id, username, password_hash FROM Users WHERE username = ?', 
                                (username,))
                    user = cursor.fetchone()
                    
                    if user:
                        # En la demo las contraseñas están en texto plano
                        stored_password = user['password_hash']
                        
                        if stored_password == password:
                            # Login exitoso
                            session['user_id'] = user['user_id']
                            session['username'] = user['username']
                            
                            # Agregar banner de demostración
                            session['is_demo'] = True
                            
                            flash('Inicio de sesión exitoso (ENTORNO DE DEMOSTRACIÓN)', 'success')
                            return redirect(url_for('dashboard'))
                else:
                    # Para SQL Server
                    cursor = conn.cursor()
                    query = "SELECT TOP 1 [user_id], [username], [password_hash] FROM [Test_Users].[dbo].[Users] WHERE [username] = ?"
                    cursor.execute(query, (username,))
                    user = cursor.fetchone()
                    
                    if user:
                        # Las contraseñas en tu base de datos parecen estar en texto plano
                        # En un entorno de producción, deberías usar hashing
                        stored_password = user[2]  # password_hash es la tercera columna
                        
                        # Si las contraseñas están en texto plano:
                        if stored_password == password:
                            # Login exitoso
                            session['user_id'] = user[0]  # user_id es la primera columna
                            session['username'] = user[1]  # username es la segunda columna
                            
                            flash('Inicio de sesión exitoso', 'success')
                            return redirect(url_for('dashboard'))
                
                # Si llegamos aquí, las credenciales son incorrectas
                flash('Usuario o contraseña incorrectos', 'error')
                return redirect(url_for('index'))
                    
            except Exception as e:
                flash('Error al procesar la solicitud', 'error')
                logger.error(f"Error durante el login: {e}")
                return redirect(url_for('index'))
            finally:
                conn.close()
        else:
            flash('Error de conexión a la base de datos', 'error')
            return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    # Proteger la ruta para usuarios autenticados
    if 'user_id' not in session:
        flash('Debe iniciar sesión para acceder', 'error')
        return redirect(url_for('index'))
    
    is_demo = session.get('is_demo', False)
    
    return render_template('dashboard.html', 
                          username=session.get('username'),
                          is_demo=is_demo)

@app.route('/logout')
def logout():
    session.clear()
    flash('Ha cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Verificar entorno
    if IS_RENDER:
        # Configuración para Render
        port = int(os.getenv('PORT', 10000))
        app.run(host='0.0.0.0', port=port)
    else:
        # Desarrollo local
        app.run(debug=True)