from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
# Esta clave es necesaria para que el login funcione en Render
app.secret_key = 'clave_secreta_maqueta_las_vegas' 
CORS(app)

# --- CONFIGURACIÓN DE LOGIN ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- USUARIOS PERMITIDOS (Opción A: Correos inventados) ---
# Aquí puedes añadir o quitar a quien quieras que entre en tu maqueta
users_db = {
    "admin@parking.com": {
        "password": generate_password_hash("1234"), 
        "nombre": "Administrador"
    },
    "invitado@parking.com": {
        "password": generate_password_hash("abcd"), 
        "nombre": "Invitado"
    }
}

class User(UserMixin):
    def __init__(self, email):
        self.id = email
        self.nombre = users_db[email]['nombre']

@login_manager.user_loader
def load_user(user_id):
    if user_id not in users_db:
        return None
    return User(user_id)

# --- RUTAS DE NAVEGACIÓN ---

@app.route('/')
@login_required
def index():
    # Corregido de 'parking.html' a 'index.html'
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user_data = users_db.get(email)
        
        if user_data and check_password_hash(user_data['password'], password):
            user = User(email)
            login_user(user, remember=remember)
            return redirect(url_for('index'))
        else:
            flash('Acceso denegado: Credenciales incorrectas')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- RUTA DE DATOS (ARDUINO / SENSORES) ---

@app.route('/status')
@login_required
def status():
    """
    MODO REAL: Aquí es donde tu Arduino enviará los datos.
    He puesto todos a 0 (Libre) para quitar la simulación.
    """
    # Cuando conectes el Arduino, esta variable 'estados' se llenará 
    # con los valores que lea tu placa.
    estados = { 
        "p2": 0, 
        "p3": 0, 
        "p4": 0, 
        "p5": 0, 
        "p6": 0, 
        "p7": 0 
    }
    return jsonify(estados)

if __name__ == '__main__':
    app.run(debug=True)
