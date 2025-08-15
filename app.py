from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
import pyodbc
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_muy_segura'  # Cambiar en producción

# Configuración de la conexión a SQL Server
SERVER = 'jp-sql-06'  # Nombre del servidor (según la imagen)
DATABASE = 'Test_Users'  # Nombre de la base de datos (según la imagen)
# Si usas autenticación Windows, no necesitas USERNAME y PASSWORD
# USERNAME = 'tu_usuario'
# PASSWORD = 'tu_contraseña'

def get_db_connection():
    """Establece y devuelve una conexión a la base de datos SQL Server"""
    try:
        # Para autenticación de Windows
        conn_str = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'
        
        # Para autenticación SQL, descomenta estas líneas y comenta la anterior
        # conn_str = f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
        
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
        return None

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
                cursor = conn.cursor()
                # Usamos parámetros para prevenir inyección SQL
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
                    else:
                        # Credenciales incorrectas
                        flash('Usuario o contraseña incorrectos', 'error')
                        return redirect(url_for('index'))
                else:
                    # Usuario no encontrado
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
    
    return render_template('dashboard.html', 
                          username=session.get('username'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Ha cerrado sesión correctamente', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)